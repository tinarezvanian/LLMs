"""Teaser scene 6 — CTA. SubQ wordmark, full breakdown, end card."""

from manim import *

from vid.theme import apply_dark_theme, body, caption, SUBQ_FG, SUBQ_GREEN, SUBQ_MUTED, PACE_NORMAL
from vid.lib.mobjects import SubQWordmark


class Scene06CTA(Scene):
    def construct(self):
        apply_dark_theme(self)

        wordmark = SubQWordmark(scale=1.4).to_edge(UP, buff=1.5)
        cta = body("Full breakdown below", color=SUBQ_GREEN).next_to(wordmark, DOWN, buff=1.0)
        handle = caption("@tinarezvanian   subq-quickstart on github", color=SUBQ_MUTED).next_to(cta, DOWN, buff=1.5)

        self.play(FadeIn(wordmark, shift=DOWN * 0.2), run_time=PACE_NORMAL)
        self.play(FadeIn(cta, shift=DOWN * 0.2), run_time=PACE_NORMAL)
        self.play(FadeIn(handle), run_time=PACE_NORMAL)
        self.wait(2.0)
