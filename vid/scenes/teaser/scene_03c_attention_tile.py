"""Teaser scene 3c — the n×n attention tile: causal mask and combinatorial growth.

Book tie-in: self-attention scratch + quadratic wall (scaling_attention).
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    text_equation,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import AttentionGrid


class Scene03CAttentionTile(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Attention materialises an n × n tile", color=SUBQ_FG).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=PACE_NORMAL)

        n = 10
        cell = 0.34
        grid = AttentionGrid(n=n, cell_size=cell, color=SUBQ_BLUE).scale(0.92).shift(DOWN * 0.35)
        self.play(FadeIn(grid, scale=0.94), run_time=PACE_SLOW)
        self.wait(0.2)
        grid.illuminate_causal(color=SUBQ_BLUE, opacity=0.55)
        self.add(grid)
        self.wait(0.45)

        mask_cap = caption("Causal LM: each row only sees ≤t (lower triangle).", color=SUBQ_MUTED).next_to(grid, DOWN, buff=0.45)
        self.play(FadeIn(mask_cap), run_time=PACE_NORMAL)
        self.wait(0.45)

        count = grid.cell_count_label().scale(0.85).next_to(grid, RIGHT, buff=0.55)
        self.play(FadeIn(count, shift=LEFT * 0.15), run_time=PACE_NORMAL)

        eq = text_equation("cells ∝ n²  (× heads × layers)", color=SUBQ_FG).scale(0.78).to_edge(DOWN, buff=0.55)
        self.play(Write(eq), run_time=PACE_SLOW)

        punch = body("n = 1M  →  10¹² cells / head / layer", color=SUBQ_MUTED).scale(0.58).next_to(eq, UP, buff=0.2)
        self.play(FadeIn(punch), run_time=PACE_NORMAL)
        self.wait(2.0)
