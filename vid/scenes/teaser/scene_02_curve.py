"""Teaser scene 2 — the curve bends. Linear becomes quadratic. n^2 floats up."""

from manim import *

from vid.theme import apply_dark_theme, body, SUBQ_BLUE, SUBQ_RED, SUBQ_MUTED, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import ScalingCurve


class Scene02Curve(Scene):
    def construct(self):
        apply_dark_theme(self)

        linear = ScalingCurve(kind="linear", color=SUBQ_BLUE)
        quadratic = ScalingCurve(kind="quadratic", color=SUBQ_RED)

        label_linear = body("what we wish AI cost", color=SUBQ_MUTED).next_to(linear, DOWN, buff=0.3)
        label_actual = body("what attention actually costs", color=SUBQ_RED).next_to(quadratic, DOWN, buff=0.3)
        n2 = MathTex("O(n^2)", font_size=72, color=SUBQ_RED).next_to(quadratic, UP, buff=0.4)

        self.add(linear, label_linear)
        self.play(Transform(linear, quadratic), Transform(label_linear, label_actual), run_time=PACE_SLOW)
        self.play(FadeIn(n2, shift=UP * 0.3), run_time=PACE_NORMAL)
        self.wait(1.0)
