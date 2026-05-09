"""Deep-dive scene 14 — on-camera close + end card with subscribe / repo / handles."""

from manim import *

from vid.theme import apply_dark_theme, body, caption, SUBQ_FG, SUBQ_GREEN, SUBQ_MUTED, PACE_NORMAL
from vid.lib.mobjects import SubQWordmark


class Scene14EndCard(Scene):
    def construct(self):
        apply_dark_theme(self)

        wordmark = SubQWordmark(scale=1.5).to_edge(UP, buff=1.5)
        cta = body("if you build with SubQ, send it to me.", color=SUBQ_FG).scale(0.7)
        cta.next_to(wordmark, DOWN, buff=1.2)
        handles = caption(
            "@tinarezvanian   |   subq-quickstart on github   |   blog: tinarezvanian.com",
            color=SUBQ_MUTED,
        ).scale(0.8)
        handles.next_to(cta, DOWN, buff=1.0)

        self.play(FadeIn(wordmark, shift=DOWN * 0.2), run_time=PACE_NORMAL)
        self.play(FadeIn(cta), run_time=PACE_NORMAL)
        self.play(FadeIn(handles), run_time=PACE_NORMAL)
        self.wait(3.0)
