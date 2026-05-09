"""Teaser scene 6 — CTA. SubQ wordmark, full breakdown, end card."""

from manim import *
from manim.utils.rate_functions import smooth

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

        sheen = Rectangle(
            height=cta.height + 0.35,
            width=0.22,
            fill_color=SUBQ_GREEN,
            fill_opacity=0.35,
            stroke_width=0,
        )
        sheen.set_opacity(0.45)
        sheen.move_to(cta.get_left() + LEFT * 1.8)
        self.add(sheen)
        self.play(sheen.animate.move_to(cta.get_right() + RIGHT * 1.8), run_time=1.25, rate_func=smooth)
        self.remove(sheen)

        self.play(FadeIn(handle), run_time=PACE_NORMAL)
        self.wait(2.0)
