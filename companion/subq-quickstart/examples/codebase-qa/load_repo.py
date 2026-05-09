"""Load an entire git repo into SubQ context and answer cross-file questions.

Usage:
    python load_repo.py /path/to/repo
    python load_repo.py /path/to/repo --question "Where do we set the HTTP timeout?"
    python load_repo.py /path/to/repo --dry-run   # measure chars loaded; no API / SDK required

This is the script the deep-dive video runs live. The whole point: no chunking,
no RAG, no retrieval pipeline. Dump the whole repo, ask the question, get the answer.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

# Lazy-import SubQ only after dry-run path — lets contributors smoke-test repo walking without SDK.

EXCLUDED_SUFFIXES = {".lock", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".bin"}
MAX_FILE_BYTES = 256 * 1024  # skip individual files larger than 256KB

app = typer.Typer(add_completion=False)
console = Console()


def collect_repo_text(root: Path) -> str:
    """Walk a git repo (respecting .gitignore via `git ls-files`) and concatenate
    the text of every reasonable source file with file-path delimiters that the
    model can use to reason about cross-file structure.
    """
    try:
        listing = subprocess.check_output(
            ["git", "ls-files"], cwd=root, text=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"`git ls-files` failed in {root}: {e}")

    chunks: list[str] = []
    for rel in listing:
        path = root / rel
        if not path.is_file():
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if len(data) > MAX_FILE_BYTES:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        chunks.append(f"\n\n===== FILE: {rel} =====\n{text}")
    return "".join(chunks)


@app.command()
def main(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, resolve_path=True),
    question: str = typer.Option(
        "Summarize the architecture of this codebase in 5 bullet points.",
        "--question",
        "-q",
        help="The question to ask about the repo.",
    ),
    model: str = typer.Option("subq-1m-preview", "--model", "-m"),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Load and measure repo text only; do not call the API.",
    ),
):
    api_key = os.environ.get("SUBQ_API_KEY")
    if not dry_run and not api_key:
        console.print("[red]SUBQ_API_KEY is not set. Get a key from https://subq.ai[/]")
        raise typer.Exit(1)

    console.print(f"[cyan]Walking[/] {repo}")
    body = collect_repo_text(repo)
    console.print(f"[cyan]Loaded[/] {len(body):,} chars (~{len(body) // 4:,} tokens)")

    if dry_run:
        console.print("[yellow]dry-run[/]: skipping API call. Install `subq` for live queries.")
        raise typer.Exit(0)

    try:
        from subq import SubQ
    except ImportError:
        print("Install the SubQ SDK first: pip install subq", file=sys.stderr)
        raise typer.Exit(1)

    client = SubQ(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a senior engineer reading the user's codebase. "
                    "Cite file paths and line numbers when you answer."
                ),
            },
            {"role": "user", "content": f"{body}\n\n# Question\n{question}"},
        ],
    )

    console.rule("[bold green]answer[/]")
    console.print(response.output_text)


if __name__ == "__main__":
    app()
