"""Teaser scene 4 — the break. Red curve cracks; green linear curve replaces it."""

from manim import *

from vid.theme import apply_dark_theme, body, SUBQ_GREEN, SUBQ_RED, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import ScalingCurve, SubQWordmark


class Scene04Break(Scene):
    def construct(self):
        apply_dark_theme(self)

        red = ScalingCurve(kind="quadratic", color=SUBQ_RED)
        green = ScalingCurve(kind="linear", color=SUBQ_GREEN)
        self.add(red)
        self.wait(0.3)

        self.play(red.graph.animate.set_stroke(opacity=0.2), run_time=PACE_NORMAL)
        self.play(Create(green.graph), run_time=PACE_SLOW)
        self.play(FadeOut(red), run_time=PACE_NORMAL)

        wordmark = SubQWordmark(scale=0.9).to_edge(DOWN, buff=1.0)
        tagline = body("linear scaling. 12M context. 52x faster.", color=SUBQ_GREEN).next_to(wordmark, UP, buff=0.4).scale(0.7)
        self.play(FadeIn(wordmark, shift=UP * 0.2), FadeIn(tagline), run_time=PACE_NORMAL)
        self.wait(1.0)
