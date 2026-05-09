"""Load a long PDF (book-length) into SubQ and produce a structured summary.

Demonstrates the second main capability of long-context: instead of chunking
a book into 4k slices and stitching summaries (lossy), put the whole thing
in context and ask the question directly.

Usage:
    python summarize_pdf.py path/to/book.pdf
    python summarize_pdf.py book.pdf --question "What are the three main arguments?"
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import typer
from pypdf import PdfReader
from rich.console import Console

try:
    from subq import SubQ
except ImportError:
    print("Install the SubQ SDK first: pip install subq", file=sys.stderr)
    sys.exit(1)

app = typer.Typer(add_completion=False)
console = Console()


def pdf_to_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            parts.append(f"\n\n----- page {i} -----\n{page.extract_text() or ''}")
        except Exception:
            continue
    return "".join(parts)


@app.command()
def main(
    pdf: Path = typer.Argument(..., exists=True, dir_okay=False, resolve_path=True),
    question: str = typer.Option(
        "Produce a structured outline of this document with chapter-level summaries and the three most important claims.",
        "--question",
        "-q",
    ),
    model: str = typer.Option("subq-1m-preview", "--model", "-m"),
):
    api_key = os.environ.get("SUBQ_API_KEY")
    if not api_key:
        console.print("[red]SUBQ_API_KEY is not set. Get a key from https://subq.ai[/]")
        raise typer.Exit(1)

    console.print(f"[cyan]Extracting[/] {pdf.name}")
    body = pdf_to_text(pdf)
    console.print(f"[cyan]Loaded[/] {len(body):,} chars (~{len(body) // 4:,} tokens)")

    client = SubQ(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a careful research assistant. Cite page numbers when "
                    "you make a factual claim about the document."
                ),
            },
            {"role": "user", "content": f"{body}\n\n# Question\n{question}"},
        ],
    )

    console.rule("[bold green]answer[/]")
    console.print(response.output_text)


if __name__ == "__main__":
    app()
