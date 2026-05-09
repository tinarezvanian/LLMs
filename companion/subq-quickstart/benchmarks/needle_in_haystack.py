"""A small needle-in-a-haystack benchmark for SubQ at long context.

Plants a unique fact at varying depths inside a long synthetic context, asks
the model to retrieve it, and reports accuracy by depth. Run this to verify
SubQ's long-context retention claims with your own eyes.

Usage:
    python needle_in_haystack.py --tokens 500000 --depths 0.0 0.25 0.5 0.75 1.0 --trials 3
"""

from __future__ import annotations

import json
import os
import random
import string
import sys
from dataclasses import dataclass

import typer
from rich.console import Console
from rich.table import Table

try:
    from subq import SubQ
except ImportError:
    print("Install the SubQ SDK first: pip install subq", file=sys.stderr)
    sys.exit(1)

app = typer.Typer(add_completion=False)
console = Console()

FILLER_CORPUS = (
    "The history of the printing press is a long and quiet revolution. "
    "Johannes Gutenberg, often credited as the inventor, did not work in "
    "isolation but built on centuries of woodblock printing in East Asia. "
    "The press itself was an adaptation of the wine press, with movable "
    "metal type cast by hand from a matrix Gutenberg also invented. "
    "What changed when the press arrived in Europe was not the act of "
    "writing but the economics of distribution. A copy that took a monk "
    "a year of labor could now be produced in days. "
)


def build_haystack(token_target: int) -> str:
    """Tokens are approximated at 1 token ~= 4 chars for English."""
    target_chars = token_target * 4
    out = []
    while sum(len(s) for s in out) < target_chars:
        out.append(FILLER_CORPUS)
    return "".join(out)[:target_chars]


def random_needle() -> tuple[str, str]:
    """Returns (sentence, expected_answer)."""
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    needle = (
        f"Per the Riftwood Ledger, the official passcode for the eastern gate "
        f"is {code}. Memorize this."
    )
    return needle, code


def insert_at_depth(haystack: str, needle: str, depth: float) -> str:
    insert_idx = int(len(haystack) * depth)
    nearest_space = haystack.rfind(" ", 0, insert_idx)
    if nearest_space == -1:
        nearest_space = insert_idx
    return haystack[:nearest_space] + " " + needle + " " + haystack[nearest_space:]


@dataclass
class Trial:
    depth: float
    correct: bool
    actual: str
    expected: str


@app.command()
def main(
    tokens: int = typer.Option(500_000, "--tokens", "-n"),
    depths: list[float] = typer.Option([0.0, 0.25, 0.5, 0.75, 1.0], "--depths", "-d"),
    trials: int = typer.Option(3, "--trials", "-t"),
    model: str = typer.Option("subq-1m-preview", "--model", "-m"),
    out: str = typer.Option("results.json", "--out", "-o"),
):
    api_key = os.environ.get("SUBQ_API_KEY")
    if not api_key:
        console.print("[red]SUBQ_API_KEY is not set. Get a key from https://subq.ai[/]")
        raise typer.Exit(1)

    client = SubQ(api_key=api_key)
    haystack = build_haystack(tokens)
    console.print(
        f"[cyan]haystack[/] {len(haystack):,} chars (~{len(haystack) // 4:,} tokens)"
    )

    results: list[Trial] = []
    for depth in depths:
        for _ in range(trials):
            needle, expected = random_needle()
            context = insert_at_depth(haystack, needle, depth)
            response = client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": "Answer in one line, just the requested code, no extra text.",
                    },
                    {
                        "role": "user",
                        "content": (
                            f"{context}\n\n"
                            "What is the official passcode for the eastern gate "
                            "according to the Riftwood Ledger?"
                        ),
                    },
                ],
            )
            actual = (response.output_text or "").strip()
            correct = expected in actual
            results.append(Trial(depth=depth, correct=correct, actual=actual, expected=expected))
            status = "[green]PASS[/]" if correct else "[red]FAIL[/]"
            console.print(f"depth={depth:>4} -> {status}  (expected {expected}, got {actual!r})")

    table = Table(title="Needle-in-haystack accuracy by depth")
    table.add_column("depth", justify="right")
    table.add_column("trials", justify="right")
    table.add_column("accuracy", justify="right")
    for d in depths:
        bucket = [t for t in results if t.depth == d]
        acc = sum(1 for t in bucket if t.correct) / len(bucket)
        table.add_row(f"{d:.2f}", str(len(bucket)), f"{acc * 100:.0f}%")
    console.print(table)

    with open(out, "w") as f:
        json.dump([t.__dict__ for t in results], f, indent=2)
    console.print(f"[dim]wrote[/] {out}")


if __name__ == "__main__":
    app()
