"""Teaser scene 3e — Chinchilla: tokens and parameters grow together at the optimum.

Book tie-in: Chinchilla isoflops / D ≈ 20N (docs/scaling_attention).
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
    SUBQ_GREEN,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene03EChinchillaBite(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Chinchilla moved the optimum", color=SUBQ_FG).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=PACE_NORMAL)

        rule = text_equation("D ≈ 20 × N", color=SUBQ_GREEN).scale(1.05).next_to(title, DOWN, buff=0.55)
        gloss = caption("D = training tokens seen, N = non-embedding parameters", color=SUBQ_MUTED).next_to(rule, DOWN, buff=0.25)
        self.play(Write(rule), FadeIn(gloss), run_time=PACE_SLOW)
        self.wait(0.45)

        rows = VGroup(
            body("Kaplan-era GPT-3 shape: huge N, comparatively few D", color=SUBQ_YELLOW).scale(0.58),
            body("Compute-optimal recipe: scale data with parameters", color=SUBQ_FG).scale(0.58),
            body("Serving economics: often over-train smaller N for cheap inference", color=SUBQ_MUTED).scale(0.56),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(gloss, DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.08) for r in rows], lag_ratio=0.2), run_time=PACE_SLOW)
        self.wait(0.5)

        eq2 = text_equation("C ≈ 6 · N · D   (training FLOPs, rule of thumb)", color=SUBQ_FG).scale(0.62).to_edge(DOWN, buff=0.85)
        self.play(Write(eq2), run_time=PACE_SLOW)
        self.wait(2.0)
