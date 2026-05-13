"""SubQ video theme — palette, fonts, and pacing constants shared across scenes.

Both the teaser and deep-dive import from here so we can iterate the look in one place.

Typography:
    - Display / body: **Alegreya Sans** when ``AlegreyaSans-*.ttf`` files are present
      under ``docs/Alegreya_Sans/``, ``docs/scaling_attention/fonts/``, or
      ``assets/branding/fonts/Alegreya_Sans/`` (same sources as the LaTeX companion).
    - Code / monospace: **JetBrains Mono** (jb/JetBrainsMono, SIL OFL) from
      ``assets/branding/fonts/``. Used for ``mono(...)``, ``code(...)``, and
      ``text_equation(...)``.

``register_font`` is called once at import time for every TTF we ship or discover.
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

FONT_MONO = "JetBrains Mono"

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FONT_DIR = _REPO_ROOT / "assets" / "branding" / "fonts"

# Same face as docs/scaling_attention (preamble.tex). Pango family name inside the TTFs.
_ALEGREYA_FAMILY = "Alegreya Sans"
_ALEGREYA_SEARCH_DIRS = (
    _REPO_ROOT / "docs" / "Alegreya_Sans",
    _REPO_ROOT / "docs" / "scaling_attention" / "fonts",
    _FONT_DIR / "Alegreya_Sans",
)


def _discover_alegreya_ttfs() -> list[Path]:
    """Return sorted unique paths to Alegreya Sans TTFs if any are vendored."""
    found: list[Path] = []
    for d in _ALEGREYA_SEARCH_DIRS:
        if not d.is_dir():
            continue
        found.extend(d.glob("AlegreyaSans*.ttf"))
        found.extend(d.glob("alegreyasans*.ttf"))
    seen: set[str] = set()
    uniq: list[Path] = []
    for p in sorted(found, key=lambda x: x.name.lower()):
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq


_ALEGREYA_TTFS = _discover_alegreya_ttfs()
if _ALEGREYA_TTFS:
    FONT_SANS = _ALEGREYA_FAMILY
    FONT_SANS_DISPLAY = _ALEGREYA_FAMILY
else:
    FONT_SANS = "Inter"
    FONT_SANS_DISPLAY = "Inter Display"

USE_ALEGREYA_SANS = bool(_ALEGREYA_TTFS)


def _activate_repo_fonts() -> None:
    """Register sans (Alegreya or Inter) + JetBrains Mono with Pango for this process."""
    stack = ExitStack()
    files: list[Path] = []
    if _ALEGREYA_TTFS:
        files.extend(_ALEGREYA_TTFS)
    else:
        files.extend(
            [
                _FONT_DIR / "Inter" / "Inter-Regular.ttf",
                _FONT_DIR / "Inter" / "Inter-Medium.ttf",
                _FONT_DIR / "Inter" / "Inter-SemiBold.ttf",
                _FONT_DIR / "Inter" / "Inter-Bold.ttf",
                _FONT_DIR / "Inter" / "InterDisplay-SemiBold.ttf",
                _FONT_DIR / "Inter" / "InterDisplay-Bold.ttf",
            ]
        )
    files.extend(
        [
            _FONT_DIR / "JetBrainsMono" / "JetBrainsMono-Regular.ttf",
            _FONT_DIR / "JetBrainsMono" / "JetBrainsMono-Medium.ttf",
            _FONT_DIR / "JetBrainsMono" / "JetBrainsMono-Bold.ttf",
        ]
    )
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
