"""Teaser scene 3b — tokens: vocabulary V, hidden d, and why the last layer hurts.

Book tie-in: token economics and output projection (docs/scaling_attention ch. on tokens).
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    mono,
    text_equation,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene03BTokens(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Every bill is in tokens", color=SUBQ_FG).to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=PACE_NORMAL)
        self.wait(0.35)

        line1 = body("Vocabulary V  (often 50k–128k)", color=SUBQ_FG).next_to(title, DOWN, buff=0.55).align_to(title, LEFT)
        line2 = body("Hidden width d  (thousands of dims)", color=SUBQ_FG).next_to(line1, DOWN, buff=0.35).align_to(line1, LEFT)
        line3 = body("Last layer: one matmul  →  V × d per token", color=SUBQ_YELLOW).next_to(line2, DOWN, buff=0.45).align_to(line1, LEFT)
        self.play(FadeIn(line1, shift=RIGHT * 0.1), run_time=PACE_NORMAL)
        self.play(FadeIn(line2, shift=RIGHT * 0.1), run_time=PACE_NORMAL)
        self.play(FadeIn(line3, shift=RIGHT * 0.1), run_time=PACE_SLOW)
        self.wait(0.5)

        eq = text_equation("per-token cost ∝ V · d", color=SUBQ_BLUE).scale(0.85).next_to(line3, DOWN, buff=0.55)
        self.play(Write(eq), run_time=PACE_SLOW)
        self.wait(0.45)

        foot = caption(
            "Vendor '1M context' means 1M tokens — not pages, not words.",
            color=SUBQ_MUTED,
        ).to_edge(DOWN, buff=0.75)
        self.play(FadeIn(foot, shift=UP * 0.12), run_time=PACE_NORMAL)

        ex = mono("Example: V=128k, d=4k  →  ~5e8 MACs / token (last layer alone)", color=SUBQ_MUTED).scale(0.52)
        ex.next_to(foot, UP, buff=0.35)
        self.play(FadeIn(ex), run_time=PACE_NORMAL)
        self.wait(2.2)
