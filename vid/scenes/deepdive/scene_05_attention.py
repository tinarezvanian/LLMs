"""Deep-dive scene 5 — attention from scratch.

Builds Q/K/V matrices, shows the softmax(QK^T/sqrt(d))V equation, materializes
the n x n attention grid, highlights cells, lands on O(n^2 d) and the trillion-
cells callout.

Reconciles two earlier drafts (canonical + scene_05_attention_grid alt) into
one scene that has both the equation and the grid + highlights.
"""

from manim import *
import numpy as np

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    text_equation,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import AttentionGrid


class Scene05Attention(Scene):
    def construct(self):
        apply_dark_theme(self)

        n = 8
        cell = 0.45

        def make_matrix(label_text: str, color: str, shift_vec: np.ndarray) -> VGroup:
            outline = Rectangle(height=n * cell, width=cell, stroke_color=color, stroke_width=2)
            label = caption(label_text, color=color).next_to(outline, UP, buff=0.15)
            grp = VGroup(outline, label).shift(shift_vec)
            return grp

        q = make_matrix("Q  [n x d]", SUBQ_BLUE, LEFT * 4)
        k = make_matrix("K  [n x d]", SUBQ_YELLOW, ORIGIN)
        v = make_matrix("V  [n x d]", SUBQ_FG, RIGHT * 4)
        self.play(FadeIn(q), FadeIn(k), FadeIn(v), run_time=PACE_NORMAL)
        self.wait(0.3)

        # LaTeX-free: matches vid/theme.text_equation — renders without preview.sty.
        eq_full = text_equation("A = softmax((Q·Kᵀ) / √d) · V", color=SUBQ_FG).scale(0.72)
        eq_full.to_edge(DOWN, buff=0.8)
        self.play(Write(eq_full), run_time=PACE_SLOW)
        self.wait(0.5)

        grid = AttentionGrid(n=n, cell_size=cell, color=SUBQ_BLUE).move_to(ORIGIN)
        self.play(
            FadeOut(q),
            FadeOut(k),
            FadeOut(v),
            FadeOut(eq_full),
            FadeIn(grid, scale=0.8),
            run_time=PACE_SLOW,
        )

        anims = []
        for i in range(n):
            for j in range(i, min(i + 3, n)):
                anims.append(grid.highlight_cell(i, j, color=SUBQ_YELLOW, opacity=0.6))
        self.play(LaggedStart(*anims, lag_ratio=0.04), run_time=PACE_SLOW)

        eq = text_equation("O(n² · d)", color=SUBQ_FG).scale(1.1).to_edge(DOWN, buff=0.7)
        self.play(Write(eq), run_time=PACE_NORMAL)

        callout = body("at n=1M  ->  10^12 cells per head per layer", color=SUBQ_MUTED).scale(0.6)
        callout.next_to(eq, DOWN, buff=0.2)
        self.play(FadeIn(callout), run_time=PACE_NORMAL)
        self.wait(1.5)
