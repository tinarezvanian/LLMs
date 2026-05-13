"""Teaser scene 3g — post-transformer frame: routing × scaling quadrant.

Book tie-in: 2×2 quadrant + SSA / alternatives (docs/scaling_attention).
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    source_footnote,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_GREEN,
    SUBQ_CYAN,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import QuadrantMap


class Scene03GLandscapeQuadrant(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Where new architectures claim to live", color=SUBQ_FG).to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=PACE_NORMAL)

        qmap = QuadrantMap(width=6.4, height=4.35).scale(0.92).shift(DOWN * 0.15)
        self.play(FadeIn(qmap.cross), run_time=PACE_NORMAL)
        self.play(
            FadeIn(qmap.routing_title),
            FadeIn(qmap.scaling_title),
            FadeIn(qmap.label_pf),
            FadeIn(qmap.label_cd),
            FadeIn(qmap.label_quad),
            FadeIn(qmap.label_lin),
            run_time=PACE_SLOW,
        )
        self.wait(0.35)

        tag = body("Subquadratic Sparse Attention (SSA)", color=SUBQ_GREEN).scale(0.62).next_to(qmap, DOWN, buff=0.45)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=PACE_NORMAL)

        br = qmap.quadrant_bg[3]
        self.play(br.animate.set_fill(SUBQ_CYAN, opacity=0.22), run_time=PACE_NORMAL)
        self.play(br.animate.set_fill(SUBQ_CYAN, opacity=0.10), run_time=PACE_NORMAL)

        foot = source_footnote("Vendor claims need independent checks — benchmarks move fast.").to_edge(DOWN, buff=0.45)
        self.play(FadeIn(foot), run_time=PACE_NORMAL)
        self.wait(2.0)
