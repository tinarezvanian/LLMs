"""SubQ video theme — palette, fonts, and pacing constants shared across scenes.

Both the teaser and deep-dive import from here so we can iterate the look in one place.
"""

from manim import *

SUBQ_BG = "#0B1020"
SUBQ_FG = "#E8ECF7"
SUBQ_MUTED = "#7A8299"
SUBQ_GREEN = "#3DDC97"
SUBQ_RED = "#FF5A5F"
SUBQ_BLUE = "#5C9EFF"
SUBQ_YELLOW = "#F5C451"
SUBQ_PURPLE = "#A77BFF"

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


def apply_dark_theme(scene: Scene) -> None:
    """Set the SubQ dark background on a scene. Call at the start of construct()."""
    scene.camera.background_color = SUBQ_BG


def title(text: str, color: str = SUBQ_FG) -> Text:
    return Text(text, font_size=TITLE_SIZE, color=color, weight=BOLD)


def heading(text: str, color: str = SUBQ_FG) -> Text:
    return Text(text, font_size=HEADING_SIZE, color=color, weight=BOLD)


def body(text: str, color: str = SUBQ_FG) -> Text:
    return Text(text, font_size=BODY_SIZE, color=color)


def caption(text: str, color: str = SUBQ_MUTED) -> Text:
    return Text(text, font_size=CAPTION_SIZE, color=color)


def equation(tex: str, color: str = SUBQ_FG) -> MathTex:
    """LaTeX-rendered equation. Requires system LaTeX with the 'preview' package.

    If your machine lacks LaTeX (or `preview.sty`), use ``text_equation()`` instead
    or run ``make setup-latex`` for install commands.
    """
    return MathTex(tex, font_size=EQUATION_SIZE, color=color)


def text_equation(plain: str, color: str = SUBQ_FG) -> Text:
    """LaTeX-free fallback for ``equation()``.

    Renders the equation as a plain ``Text`` mobject using Unicode (e.g. ``"O(n²)"``,
    ``"h_t = A·h_{t-1} + B·x_t"``). Use this on machines without LaTeX, or when you
    want a quick layout pass before installing the LaTeX preview package.
    """
    return Text(plain, font_size=EQUATION_SIZE, color=color, weight=BOLD)


def source_footnote(text: str) -> Text:
    """Tiny attribution label for benchmark numbers, citations, etc."""
    t = Text(text, font_size=18, color=SUBQ_MUTED, slant=ITALIC)
    return t
