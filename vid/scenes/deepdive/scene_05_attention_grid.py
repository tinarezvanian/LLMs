"""Deep-dive scene 5 — attention from scratch. Q, K, V, then the n x n grid forms."""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    heading,
    caption,
    equation,
    SUBQ_FG,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    SUBQ_MUTED,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import AttentionGrid


class Scene05AttentionGrid(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Attention is an n x n matrix", color=SUBQ_FG).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        q = self._labeled_matrix("Q", "[n x d]").to_edge(LEFT, buff=1.0)
        k = self._labeled_matrix("K", "[n x d]").next_to(q, RIGHT, buff=1.0)
        v = self._labeled_matrix("V", "[n x d]").next_to(k, RIGHT, buff=1.0)

        self.play(LaggedStart(FadeIn(q), FadeIn(k), FadeIn(v), lag_ratio=0.3), run_time=PACE_SLOW)
        self.wait(0.5)

        eq = equation(r"A = \mathrm{softmax}\!\left(\frac{Q K^{\!\top}}{\sqrt{d}}\right) V").scale(0.85)
        eq.to_edge(DOWN, buff=1.3)
        self.play(Write(eq), run_time=PACE_SLOW)

        grid = AttentionGrid(n=8, cell_size=0.4, color=SUBQ_BLUE).next_to(eq, UP, buff=0.4)
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in grid.cells.values()], lag_ratio=0.005), run_time=PACE_SLOW)

        size_label = body("size = n^2", color=SUBQ_YELLOW).scale(0.7).next_to(grid, RIGHT, buff=0.5)
        self.play(FadeIn(size_label, shift=LEFT * 0.2), run_time=PACE_NORMAL)
        self.wait(1.5)

    def _labeled_matrix(self, name: str, shape: str) -> VGroup:
        rect = Rectangle(width=1.6, height=2.2, stroke_color=SUBQ_BLUE, stroke_width=3, fill_color=SUBQ_BLUE, fill_opacity=0.05)
        n = body(name, color=SUBQ_BLUE).scale(0.8).move_to(rect.get_center() + UP * 0.3)
        s = caption(shape, color=SUBQ_MUTED).scale(0.6).move_to(rect.get_center() + DOWN * 0.4)
        return VGroup(rect, n, s)
