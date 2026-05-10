"""SubQ video theme — palette, fonts, and pacing constants shared across scenes.

Both the teaser and deep-dive import from here so we can iterate the look in one place.

Typography:
    - Display / body: **Inter** (rsms/inter, SIL OFL). Crisp at 1080p, optimized for
      screens, tabular numerals — perfect for benchmark callouts.
    - Code / monospace: **JetBrains Mono** (jb/JetBrainsMono, SIL OFL). Used for
      anything inside ``mono(...)`` or ``code(...)`` (KV cache equations, terminal
      readouts, file paths in screen-capture overlays).

Both font families ship inside this repo at ``assets/branding/fonts/`` so renders
work on a clean checkout without any system font install. ``register_font`` is
called once at import time.
"""

from __future__ import annotations

import atexit
from contextlib import ExitStack
from pathlib import Path

from manim import *
from manim import register_font

SUBQ_BG = "#0B1020"
SUBQ_FG = "#E8ECF7"
SUBQ_MUTED = "#7A8299"
SUBQ_GREEN = "#3DDC97"
SUBQ_RED = "#FF5A5F"
SUBQ_BLUE = "#5C9EFF"
SUBQ_YELLOW = "#F5C451"
SUBQ_PURPLE = "#A77BFF"
SUBQ_CYAN = "#2DD4BF"  # SSA / accent dot on quadrant maps

GOOD = SUBQ_GREEN
BAD = SUBQ_RED
NEUTRAL = SUBQ_BLUE
ACCENT = SUBQ_YELLOW
HIGHLIGHT = SUBQ_PURPLE

TITLE_SIZE = 56
HEADING_SIZE = 40
BODY_SIZE = 32
CAPTION_SIZE = 24
EQUATION_SIZE = 44

PACE_FAST = 0.4
PACE_NORMAL = 0.8
PACE_SLOW = 1.5
PACE_BEAT = 0.6

FONT_SANS = "Inter"
FONT_SANS_DISPLAY = "Inter Display"
FONT_MONO = "JetBrains Mono"

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FONT_DIR = _REPO_ROOT / "assets" / "branding" / "fonts"


def _activate_repo_fonts() -> None:
    """Register Inter + JetBrains Mono with Pango for the lifetime of this process.

    Manim's ``register_font`` returns a context manager. We hold the contexts
    open in a module-level ``ExitStack`` and close them on interpreter shutdown
    so every scene file imported under this process sees the fonts.

    Silently no-ops if a TTF is missing so a partial checkout still renders
    (Pango will fall back to system sans).
    """
    stack = ExitStack()
    files = [
        _FONT_DIR / "Inter" / "Inter-Regular.ttf",
        _FONT_DIR / "Inter" / "Inter-Medium.ttf",
        _FONT_DIR / "Inter" / "Inter-SemiBold.ttf",
        _FONT_DIR / "Inter" / "Inter-Bold.ttf",
        _FONT_DIR / "Inter" / "InterDisplay-SemiBold.ttf",
        _FONT_DIR / "Inter" / "InterDisplay-Bold.ttf",
        _FONT_DIR / "JetBrainsMono" / "JetBrainsMono-Regular.ttf",
        _FONT_DIR / "JetBrainsMono" / "JetBrainsMono-Medium.ttf",
        _FONT_DIR / "JetBrainsMono" / "JetBrainsMono-Bold.ttf",
    ]
    for ttf in files:
        if not ttf.exists():
            continue
        try:
            stack.enter_context(register_font(str(ttf)))
        except Exception:
            # Pango may already have it from a previous import or from system
            # install — in either case keep going so renders don't blow up.
            pass
    atexit.register(stack.close)


_activate_repo_fonts()


def apply_dark_theme(scene: Scene) -> None:
    """Set the SubQ dark background on a scene. Call at the start of construct()."""
    scene.camera.background_color = SUBQ_BG


def title(text: str, color: str = SUBQ_FG) -> Text:
    return Text(text, font=FONT_SANS_DISPLAY, font_size=TITLE_SIZE, color=color, weight=BOLD)


def heading(text: str, color: str = SUBQ_FG) -> Text:
    return Text(text, font=FONT_SANS_DISPLAY, font_size=HEADING_SIZE, color=color, weight=BOLD)


def body(text: str, color: str = SUBQ_FG) -> Text:
    return Text(text, font=FONT_SANS, font_size=BODY_SIZE, color=color)


def caption(text: str, color: str = SUBQ_MUTED) -> Text:
    return Text(text, font=FONT_SANS, font_size=CAPTION_SIZE, color=color)


def mono(text: str, color: str = SUBQ_FG, size: int = BODY_SIZE) -> Text:
    """Monospaced text in JetBrains Mono. Use for code snippets, file paths,
    benchmark numbers that should align column-wise."""
    return Text(text, font=FONT_MONO, font_size=size, color=color)


# Alias kept so old imports (`from vid.theme import code`) still work.
code = mono


def equation(tex: str, color: str = SUBQ_FG) -> MathTex:
    """LaTeX-rendered equation. Requires system LaTeX with the 'preview' package.

    If your machine lacks LaTeX (or `preview.sty`), use ``text_equation()`` instead
    or run ``make setup-latex`` for install commands.
    """
    return MathTex(tex, font_size=EQUATION_SIZE, color=color)


def text_equation(plain: str, color: str = SUBQ_FG) -> Text:
    """LaTeX-free fallback for ``equation()``.

    Renders the equation as a plain ``Text`` mobject in JetBrains Mono so the
    spacing reads as math (e.g. ``"O(n²)"``, ``"h_t = A·h_{t-1} + B·x_t"``).
    Use this on machines without LaTeX, or when you want a quick layout pass
    before installing the LaTeX preview package.
    """
    return Text(plain, font=FONT_MONO, font_size=EQUATION_SIZE, color=color, weight=BOLD)


def source_footnote(text: str) -> Text:
    """Tiny attribution label for benchmark numbers, citations, etc."""
    return Text(text, font=FONT_SANS, font_size=18, color=SUBQ_MUTED, slant=ITALIC)
