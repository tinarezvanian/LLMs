"""Teaser scene 2 — the curve bends. Linear becomes quadratic. n^2 floats up."""

from manim import *
from manim.utils.rate_functions import smooth, there_and_back

from vid.theme import apply_dark_theme, body, FONT_MONO, SUBQ_BLUE, SUBQ_RED, SUBQ_MUTED, PACE_FAST, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import ScalingCurve


class Scene02Curve(Scene):
    def construct(self):
        apply_dark_theme(self)

        linear = ScalingCurve(kind="linear", color=SUBQ_BLUE)
        quadratic = ScalingCurve(kind="quadratic", color=SUBQ_RED)

        label_linear = body("what we wish AI cost", color=SUBQ_MUTED).next_to(linear, DOWN, buff=0.3)
        label_actual = body("what attention actually costs", color=SUBQ_RED).next_to(quadratic, DOWN, buff=0.3)
        # Text, not MathTex: avoids a full LaTeX install with preview.sty (MiKTeX/TeX Live).
        # Mono font keeps the parens + n + ² visually balanced.
        n2 = Text("O(n²)", font=FONT_MONO, font_size=72, color=SUBQ_RED, weight=BOLD).next_to(quadratic, UP, buff=0.4)

        self.add(linear, label_linear)
        # Micro anticipation: breathe the linear curve once before the bend.
        self.play(linear.animate.scale(1.04), label_linear.animate.shift(UP * 0.06), run_time=PACE_FAST, rate_func=there_and_back)
        self.play(
            Transform(linear, quadratic),
            Transform(label_linear, label_actual),
            run_time=PACE_SLOW,
            rate_func=smooth,
        )
        self.play(FadeIn(n2, shift=UP * 0.3), run_time=PACE_NORMAL, rate_func=smooth)
        self.wait(1.0)
