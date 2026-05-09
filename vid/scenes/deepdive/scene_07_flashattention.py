"""Deep-dive scene 7 — FlashAttention defense. Helps, but asymptote stays."""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_RED,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import ScalingCurve


class Scene07FlashAttention(Scene):
    def construct(self):
        apply_dark_theme(self)

        bare = ScalingCurve(kind="quadratic", color=SUBQ_RED).shift(UP * 0.3)
        bare_label = caption("attention  (n^2)", color=SUBQ_RED).next_to(bare, DOWN, buff=0.2)
        self.play(Create(bare), FadeIn(bare_label), run_time=PACE_NORMAL)

        flash_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=4,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        ).move_to(bare.axes)
        flash = flash_axes.plot(
            lambda x: min(x * x / 18.0, 6.0), x_range=[0.01, 6], color=SUBQ_YELLOW, stroke_width=4
        )
        flash_label = caption("FlashAttention  (still n^2, smaller constant)", color=SUBQ_YELLOW).next_to(
            bare, UP, buff=0.4
        )
        self.play(Create(flash), FadeIn(flash_label), run_time=PACE_SLOW)

        kicker = body("the asymptote stays", color=SUBQ_FG).scale(0.8).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(kicker, shift=UP * 0.2), run_time=PACE_NORMAL)
        self.wait(1.5)
