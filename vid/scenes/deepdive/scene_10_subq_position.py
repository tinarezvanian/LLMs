"""Deep-dive scene 10 — script Scene 9: 2×2 routing × scaling quadrant (where SubQ fits).

Replaces the old PostTransformerTree branch visual. See scripts/deepdive.md Scene 9 [ANIM].
"""

from __future__ import annotations

import numpy as np
from manim import *

from vid.theme import (
    apply_dark_theme,
    caption,
    heading,
    source_footnote,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    SUBQ_RED,
    SUBQ_CYAN,
    PACE_FAST,
    PACE_NORMAL,
    PACE_SLOW,
    FONT_SANS,
    FONT_MONO,
)
from vid.lib.mobjects import AttentionGrid, QuadrantMap, SubQWordmark


class Scene10SubQPosition(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("two axes that matter", color=SUBQ_FG).scale(0.85).to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=PACE_NORMAL)

        quad = QuadrantMap(width=6.4, height=4.2).scale(0.92).shift(UP * 0.35)

        self.play(
            FadeIn(quad.cross),
            FadeIn(quad.routing_title),
            FadeIn(quad.scaling_title),
            run_time=PACE_SLOW,
        )
        self.play(
            LaggedStart(
                FadeIn(quad.label_pf, shift=RIGHT * 0.2),
                FadeIn(quad.label_cd, shift=LEFT * 0.2),
                FadeIn(quad.label_quad, shift=DOWN * 0.15),
                FadeIn(quad.label_lin, shift=UP * 0.15),
                lag_ratio=0.25,
            ),
            run_time=PACE_SLOW,
        )
        self.wait(0.2)

        self.play(
            quad.label_pf.animate.set_color(SUBQ_YELLOW),
            quad.label_cd.animate.set_color(SUBQ_GREEN),
            run_time=PACE_FAST,
        )
        self.play(
            quad.label_pf.animate.set_color(SUBQ_MUTED),
            quad.label_cd.animate.set_color(SUBQ_MUTED),
            run_time=PACE_FAST,
        )
        self.play(
            quad.label_quad.animate.set_color(SUBQ_RED),
            quad.label_lin.animate.set_color(SUBQ_GREEN),
            run_time=PACE_FAST,
        )
        self.play(
            quad.label_quad.animate.set_color(SUBQ_MUTED),
            quad.label_lin.animate.set_color(SUBQ_MUTED),
            run_time=PACE_FAST,
        )

        qc = quad.get_center()
        dx = quad.width / 4
        dy = quad.height / 4

        # Top-right quadrant (content-dependent + quadratic)
        tr_dot_tf = Dot(radius=0.1, color=SUBQ_GREEN)
        tr_tf = Text(
            "Standard transformers  ·  FlashAttention",
            font=FONT_SANS,
            font_size=18,
            color=SUBQ_FG,
        ).next_to(tr_dot_tf, RIGHT, buff=0.15)
        tr_orange = Dot(radius=0.08, color=SUBQ_YELLOW).next_to(tr_tf, DOWN, aligned_edge=LEFT, buff=0.18)
        tr_ds = Text(
            "DeepSeek Sparse Attention*",
            font=FONT_SANS,
            font_size=17,
            color=SUBQ_YELLOW,
        ).next_to(tr_orange, RIGHT, buff=0.12)
        tr_fn = source_footnote("* indexer still O(n²) in worst case").scale(0.85)
        tr_fn.next_to(tr_ds, DOWN, aligned_edge=LEFT, buff=0.08)
        tr_stack = VGroup(tr_dot_tf, tr_tf, tr_orange, tr_ds, tr_fn)
        tr_stack.move_to(qc + UP * dy + RIGHT * dx + LEFT * 0.35 + DOWN * 0.15)
        self.play(FadeIn(tr_stack, shift=UP * 0.1), run_time=PACE_NORMAL)
        self.wait(0.15)

        bl_dot = Dot(radius=0.09, color=SUBQ_YELLOW)
        bl_txt = Text(
            "Sliding window  ·  Longformer  ·  BigBird  ·  Mistral SWA",
            font=FONT_SANS,
            font_size=17,
            color=SUBQ_YELLOW,
        ).next_to(bl_dot, RIGHT, buff=0.12)
        bl_stack = VGroup(bl_dot, bl_txt)
        bl_stack.move_to(qc + DOWN * dy + LEFT * dx + RIGHT * 0.25 + UP * 0.12)
        self.play(FadeIn(bl_stack, shift=DOWN * 0.1), run_time=PACE_NORMAL)
        self.wait(0.15)

        br_grey = Dot(radius=0.09, color=SUBQ_MUTED)
        br_mamba = Text(
            "Mamba / SSM*",
            font=FONT_SANS,
            font_size=18,
            color=SUBQ_MUTED,
        ).next_to(br_grey, RIGHT, buff=0.12)
        br_foot = source_footnote("* lossy fixed-capacity state").scale(0.85)
        br_foot.next_to(br_mamba, DOWN, aligned_edge=LEFT, buff=0.06)
        br_stack = VGroup(br_grey, br_mamba, br_foot)
        br_stack.move_to(qc + DOWN * dy + RIGHT * dx + LEFT * 0.55 + UP * 0.28)

        ssa_dot = Dot(radius=0.12, color=SUBQ_CYAN)
        ssa_lab = Text(
            "SSA — Subquadratic Sparse Attention",
            font=FONT_SANS,
            font_size=19,
            color=SUBQ_CYAN,
            weight=BOLD,
        ).next_to(ssa_dot, RIGHT, buff=0.15)
        ssa_stack = VGroup(ssa_dot, ssa_lab)
        ssa_stack.move_to(qc + DOWN * dy + RIGHT * dx + RIGHT * 0.25 + DOWN * 0.42)

        self.play(FadeIn(br_stack, shift=DOWN * 0.08), run_time=PACE_NORMAL)
        self.play(FadeIn(ssa_stack, scale=0.92), run_time=PACE_SLOW)
        self.play(Flash(ssa_dot, color=SUBQ_CYAN, line_length=0.35, flash_radius=0.55), run_time=PACE_FAST)
        self.wait(0.25)

        inset = AttentionGrid(n=11, cell_size=0.28).scale(0.42)
        inset.to_corner(DR, buff=0.35)
        inset.illuminate_causal(SUBQ_BLUE, 0.55)
        inset_label = caption("dense scores all pairs", color=SUBQ_MUTED).scale(0.75)
        inset_label.next_to(inset, UP, buff=0.12)
        self.play(FadeIn(inset), FadeIn(inset_label), run_time=PACE_FAST)

        rng = np.random.default_rng(42)
        dim_anims = []
        for i in range(inset.n):
            cols = list(range(i + 1))
            n_keep = max(1, int(len(cols) * 0.08))
            keep = set(rng.choice(cols, size=n_keep, replace=False).tolist())
            for j in cols:
                if j not in keep:
                    dim_anims.append(inset.cells[(i, j)].animate.set_fill("#050812", 0.94))

        self.play(LaggedStart(*dim_anims, lag_ratio=0.004), run_time=1.8)

        sparse_lbl = caption("…only a few matter per query — SSA attends on a subset", color=SUBQ_GREEN).scale(
            0.72
        )
        sparse_lbl.next_to(inset, DOWN, buff=0.1)
        self.play(FadeOut(inset_label), run_time=PACE_FAST)
        self.play(FadeIn(sparse_lbl), run_time=PACE_FAST)

        quote = Text(
            "subq.ai/how-ssa-makes-long-context-practical — May 5, 2026",
            font=FONT_MONO,
            font_size=16,
            color=SUBQ_MUTED,
            slant=ITALIC,
        ).scale(0.78).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(quote), run_time=PACE_NORMAL)

        wordmark = SubQWordmark(scale=0.55).next_to(quote, UP, buff=0.35)
        self.play(FadeIn(wordmark, shift=UP * 0.15), run_time=PACE_NORMAL)
        self.wait(1.2)
