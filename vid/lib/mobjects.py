"""Reusable visual building blocks for the SubQ videos.

Keep anything that appears in more than one scene here. Scene-specific one-offs
should live next to the scene that uses them.
"""

from manim import *
import numpy as np

from vid.theme import (
    SUBQ_BG,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_GREEN,
    SUBQ_RED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    GOOD,
    BAD,
    NEUTRAL,
    ACCENT,
    FONT_SANS,
    FONT_SANS_DISPLAY,
    FONT_MONO,
)


class SubQWordmark(VGroup):
    """A simple text-based SubQ wordmark. Replace with a vectorized SVG before final render."""

    def __init__(self, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        sub = Text("Sub", font=FONT_SANS_DISPLAY, font_size=72, color=SUBQ_FG, weight=BOLD)
        q = Text("Q", font=FONT_SANS_DISPLAY, font_size=72, color=SUBQ_GREEN, weight=BOLD)
        q.next_to(sub, RIGHT, buff=0.05)
        self.add(sub, q)
        self.scale(scale)


class AttentionGrid(VGroup):
    """An n-by-n grid that visually represents the attention matrix.

    Cells can be lit up via .highlight_cell() to show particular attention patterns.
    Used heavily in deep-dive scene 5 (attention from scratch) and scene 7 (FlashAttention).
    """

    def __init__(self, n: int = 8, cell_size: float = 0.4, color: str = SUBQ_BLUE, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.cell_size = cell_size
        self.cells = {}
        for i in range(n):
            for j in range(n):
                cell = Square(side_length=cell_size, stroke_width=1.0, stroke_color=color)
                cell.set_fill(SUBQ_BG, opacity=0.0)
                cell.move_to(np.array([j * cell_size, -i * cell_size, 0]))
                self.cells[(i, j)] = cell
                self.add(cell)
        self.move_to(ORIGIN)

    def highlight_cell(self, i: int, j: int, color: str = SUBQ_YELLOW, opacity: float = 0.8):
        return self.cells[(i, j)].animate.set_fill(color, opacity=opacity)

    def cell_count_label(self) -> Text:
        return Text(f"n² = {self.n * self.n}", font=FONT_MONO, font_size=32, color=SUBQ_MUTED)


class ScalingCurve(VGroup):
    """A configurable curve for the n^2 vs n vs n log n comparisons in the teaser.

    kind is one of 'linear', 'quadratic', 'nlogn'. Plots over [x_min, x_max].
    """

    def __init__(
        self,
        kind: str = "quadratic",
        x_range=(0, 6),
        y_range=(0, 6),
        color: str = SUBQ_RED,
        stroke_width: float = 6.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        axes = Axes(
            x_range=[x_range[0], x_range[1], 1],
            y_range=[y_range[0], y_range[1], 1],
            x_length=6,
            y_length=4,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        )
        self.axes = axes

        def f(x):
            if kind == "linear":
                return x
            if kind == "quadratic":
                return min(x * x / 6.0, y_range[1])
            if kind == "nlogn":
                return x * (np.log(x + 1.0))
            raise ValueError(f"Unknown curve kind: {kind}")

        graph = axes.plot(f, x_range=[x_range[0] + 0.01, x_range[1]], color=color, stroke_width=stroke_width)
        self.graph = graph
        self.add(axes, graph)


class GPUOutline(VGroup):
    """A stylized H100 GPU outline with a labeled capacity."""

    def __init__(self, label: str = "H100  80 GB", **kwargs):
        super().__init__(**kwargs)
        body = RoundedRectangle(corner_radius=0.15, height=2.0, width=4.5, stroke_color=SUBQ_FG, stroke_width=3)
        cap = Text(label, font=FONT_MONO, font_size=22, color=SUBQ_FG)
        cap.move_to(body.get_center())
        self.add(body, cap)


class KVCacheBar(VGroup):
    """A horizontal bar that fills proportionally to KV cache size.

    fraction in [0, ...]. Anything > 1.0 visually overflows to indicate "doesn't fit on the GPU".
    """

    def __init__(self, fraction: float = 0.5, label: str = "KV cache", color: str = SUBQ_RED, **kwargs):
        super().__init__(**kwargs)
        outline = Rectangle(height=0.6, width=4.5, stroke_color=SUBQ_FG, stroke_width=2)
        fill = Rectangle(height=0.55, width=4.45 * min(fraction, 1.0), stroke_width=0, fill_color=color, fill_opacity=0.85)
        fill.align_to(outline, LEFT)
        cap = Text(f"{label}", font=FONT_SANS, font_size=20, color=SUBQ_MUTED)
        cap.next_to(outline, UP, buff=0.15)
        self.add(outline, fill, cap)
        self._outline = outline
        self._fill = fill
        self._fraction = fraction

        if fraction > 1.0:
            overflow = Rectangle(
                height=0.55,
                width=4.45 * (fraction - 1.0),
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.4,
            )
            overflow.next_to(outline, RIGHT, buff=0.0)
            self.add(overflow)


class PostTransformerTree(VGroup):
    """The 'post-transformer landscape' tree from deep-dive scene 8.

    Root: 'subquadratic sequence models'.
    Branches: SSMs, long convs, linear attention, hybrids, SubQ.
    Each branch is an attribute so scenes can highlight/animate them individually.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = Text("subquadratic sequence models", font=FONT_SANS_DISPLAY, font_size=28, color=SUBQ_FG, weight=BOLD)
        self.root = root

        branches_text = [
            ("State Space Models\n(Mamba, S4)", SUBQ_BLUE),
            ("Long Convolutions\n(Hyena)", SUBQ_YELLOW),
            ("Linear Attention\n(Performer, RetNet)", SUBQ_PURPLE := "#A77BFF"),
            ("Hybrids\n(SAMBA, Jamba, Griffin)", SUBQ_GREEN),
            ("Subquadratic Sparse Attention\n(SubQ)", SUBQ_GREEN),
        ]
        self.branches = []
        n = len(branches_text)
        spacing = 2.6
        for i, (text, color) in enumerate(branches_text):
            x = (i - (n - 1) / 2.0) * spacing
            node = Text(text, font=FONT_SANS, font_size=20, color=color, weight=BOLD)
            node.move_to(np.array([x, -2.0, 0]))
            line = Line(root.get_bottom(), node.get_top(), stroke_color=SUBQ_MUTED, stroke_width=2)
            self.branches.append((node, line))
            self.add(line, node)
        self.add(root)
