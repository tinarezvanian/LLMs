"""Deep-dive scene 7 — FlashAttention defense.

Three curves: standard attention (red), FlashAttention (yellow), subquadratic (green).
Ends with an attention-matrix inset: causal cells lit, then most dim to near-black
(\"wastefully quadratic\") — pairs with script Scene 9 / scene 10 quadrant narrative.
"""

from __future__ import annotations

import numpy as np
from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_MUTED,
    SUBQ_RED,
    SUBQ_YELLOW,
    SUBQ_BLUE,
    PACE_FAST,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import AttentionGrid


class Scene07FlashAttention(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("FlashAttention: brilliant, but still O(n²)", color=SUBQ_FG).scale(0.9).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        )
        self.play(Create(axes), run_time=PACE_NORMAL)

        attn = axes.plot(lambda x: min(x * x / 6.0, 6), x_range=[0.1, 6], color=SUBQ_RED, stroke_width=4)
        attn_label = caption("standard attention", color=SUBQ_RED).next_to(attn.get_end(), UP, buff=0.1).scale(0.8)
        self.play(Create(attn), FadeIn(attn_label), run_time=PACE_SLOW)

        flash = axes.plot(lambda x: min(x * x / 18.0, 6), x_range=[0.1, 6], color=SUBQ_YELLOW, stroke_width=4)
        flash_label = caption("FlashAttention (~3x faster, same shape)", color=SUBQ_YELLOW).scale(0.7)
        flash_label.next_to(flash.get_end(), UP, buff=0.6)
        self.play(Create(flash), FadeIn(flash_label), run_time=PACE_SLOW)

        linear = axes.plot(lambda x: 0.6 * x, x_range=[0.1, 6], color=SUBQ_GREEN, stroke_width=4)
        linear_label = caption("subquadratic (linear)", color=SUBQ_GREEN).scale(0.7)
        linear_label.next_to(linear.get_end(), DOWN, buff=0.1)
        self.play(Create(linear), FadeIn(linear_label), run_time=PACE_SLOW)

        x_label = caption("context length n", color=SUBQ_MUTED).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = caption("compute / memory", color=SUBQ_MUTED).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI / 2)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=PACE_NORMAL)

        plot_block = VGroup(axes, attn, attn_label, flash, flash_label, linear, linear_label, x_label, y_label)
        plot_block.scale(0.82).shift(UP * 0.55 + LEFT * 0.35)

        kicker = body("the asymptote stays", color=SUBQ_FG).scale(0.78).next_to(plot_block, DOWN, buff=0.35)
        self.play(FadeIn(kicker, shift=UP * 0.2), run_time=PACE_NORMAL)

        # Sparse inset: most attention weights ~ 0, still paid for with n² work
        grid = AttentionGrid(n=12, cell_size=0.26).scale(0.48)
        grid.next_to(kicker, DOWN, buff=0.28)
        grid.illuminate_causal(SUBQ_BLUE, 0.52)
        grid_note = caption("trained models: most matrix entries ≈ 0", color=SUBQ_MUTED).scale(0.72)
        grid_note.next_to(grid, UP, buff=0.12)
        self.play(FadeIn(grid), FadeIn(grid_note), run_time=PACE_FAST)

        rng = np.random.default_rng(7)
        dims = []
        for i in range(grid.n):
            cols = list(range(i + 1))
            n_keep = max(1, int(len(cols) * 0.06))
            keep = set(rng.choice(cols, size=n_keep, replace=False).tolist())
            for j in cols:
                if j not in keep:
                    dims.append(grid.cells[(i, j)].animate.set_fill("#060a14", 0.93))

        self.play(LaggedStart(*dims, lag_ratio=0.005), run_time=2.2)
        punch = body("wastefully quadratic — still compute them all", color=SUBQ_YELLOW).scale(0.62)
        punch.next_to(grid, DOWN, buff=0.14)
        self.play(FadeIn(punch, shift=UP * 0.12), run_time=PACE_FAST)
        self.wait(1.2)
