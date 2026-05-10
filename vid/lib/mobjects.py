"""Reusable visual building blocks for the SubQ videos.

Keep anything that appears in more than one scene here. Scene-specific one-offs
should live next to the scene that uses them.
"""

from __future__ import annotations

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
    SUBQ_CYAN,
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

    def illuminate_causal(self, color: str = SUBQ_BLUE, opacity: float = 0.65):
        """Fill lower-triangle (causal) cells — typical dense self-attention mask."""
        for i in range(self.n):
            for j in range(self.n):
                if j <= i:
                    self.cells[(i, j)].set_fill(color, opacity=opacity)

    def dim_sparse_pattern(
        self,
        dim_color: str = SUBQ_BG,
        dim_opacity: float = 0.92,
        bright_color: str = SUBQ_YELLOW,
        bright_opacity: float = 0.85,
        rng: np.random.Generator | None = None,
        keep_fraction: float = 0.07,
    ):
        """Fade most causal cells to near-black; keep a sparse subset bright per row.

        Illustrates 'wastefully quadratic' intuition: most weights are negligible.
        """
        rng = rng or np.random.default_rng(0)
        for i in range(self.n):
            cols = list(range(i + 1))
            n_keep = max(1, int(len(cols) * keep_fraction))
            keep = set(rng.choice(cols, size=n_keep, replace=False).tolist())
            for j in cols:
                if j in keep:
                    self.cells[(i, j)].set_fill(bright_color, opacity=bright_opacity)
                else:
                    self.cells[(i, j)].set_fill(dim_color, opacity=dim_opacity)

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


class QuadrantMap(VGroup):
    """Routing × scaling 2×2 frame (script Scene 9 / Manim scene_10).

    Axes: horizontal = routing (left: position-fixed → right: content-dependent).
          vertical = scaling (top: quadratic → bottom: linear).
    """

    def __init__(
        self,
        width: float = 6.8,
        height: float = 4.6,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.w = width
        self.h = height
        hw, hh = width / 2, height / 2

        frame = Rectangle(width=width, height=height, stroke_color=SUBQ_MUTED, stroke_width=2)
        v_mid = Line(UP * hh, DOWN * hh, stroke_color=SUBQ_MUTED, stroke_width=2)
        h_mid = Line(LEFT * hw, RIGHT * hw, stroke_color=SUBQ_MUTED, stroke_width=2)
        glow = VGroup(frame, v_mid, h_mid)

        # Faint quadrant tint (Tufte-style separation)
        tl = Rectangle(width=hw, height=hh, stroke_width=0, fill_color=SUBQ_RED, fill_opacity=0.06).shift(LEFT * hw / 2 + UP * hh / 2)
        tr = Rectangle(width=hw, height=hh, stroke_width=0, fill_color=SUBQ_GREEN, fill_opacity=0.06).shift(RIGHT * hw / 2 + UP * hh / 2)
        bl = Rectangle(width=hw, height=hh, stroke_width=0, fill_color=SUBQ_YELLOW, fill_opacity=0.06).shift(LEFT * hw / 2 + DOWN * hh / 2)
        br = Rectangle(width=hw, height=hh, stroke_width=0, fill_color=SUBQ_CYAN, fill_opacity=0.08).shift(RIGHT * hw / 2 + DOWN * hh / 2)

        self.axes_lines = glow
        self.quadrant_bg = VGroup(tl, tr, bl, br)
        self.cross = VGroup(self.quadrant_bg, glow)

        # Axis endpoint hints (slide-in targets for scenes)
        self.label_pf = Text("position-fixed", font=FONT_SANS, font_size=20, color=SUBQ_MUTED)
        self.label_pf.move_to(np.array([-hw * 0.65, -hh - 0.55, 0]))
        self.label_cd = Text("content-dependent", font=FONT_SANS, font_size=20, color=SUBQ_MUTED)
        self.label_cd.move_to(np.array([hw * 0.65, -hh - 0.55, 0]))

        self.label_quad = Text("quadratic", font=FONT_SANS, font_size=20, color=SUBQ_MUTED)
        self.label_quad.move_to(np.array([-hw - 0.85, hh * 0.65, 0]))
        self.label_lin = Text("linear", font=FONT_SANS, font_size=20, color=SUBQ_MUTED)
        self.label_lin.move_to(np.array([-hw - 0.85, -hh * 0.65, 0]))

        self.routing_title = Text(
            "routing",
            font=FONT_SANS_DISPLAY,
            font_size=22,
            color=SUBQ_FG,
            weight=BOLD,
        ).move_to(np.array([0, -hh - 1.05, 0]))
        self.scaling_title = Text(
            "scaling",
            font=FONT_SANS_DISPLAY,
            font_size=22,
            color=SUBQ_FG,
            weight=BOLD,
        ).move_to(np.array([-hw - 1.35, 0, 0])).rotate(PI / 2)

        self.add(self.cross, self.routing_title, self.scaling_title, self.label_pf, self.label_cd, self.label_quad, self.label_lin)
