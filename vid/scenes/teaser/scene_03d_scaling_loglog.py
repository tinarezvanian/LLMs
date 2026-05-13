"""Teaser scene 3d — Kaplan scaling: smooth power law on log-log axes.

Book tie-in: Kaplan et al. scaling laws (docs/scaling_attention).
"""

from manim import *
import numpy as np

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    text_equation,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene03DScalingLogLog(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Then the field found a straight line", color=SUBQ_FG).to_edge(UP, buff=0.5)
        sub = caption("Kaplan-style scaling: loss vs size on log–log axes", color=SUBQ_MUTED).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title, shift=DOWN * 0.12), FadeIn(sub), run_time=PACE_NORMAL)

        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            x_length=7.2,
            y_length=4.0,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        ).shift(DOWN * 0.35)
        xl = caption("log N", color=SUBQ_MUTED).next_to(axes.x_axis, DOWN, buff=0.25)
        yl = caption("log L", color=SUBQ_MUTED).next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), run_time=PACE_NORMAL)

        rng = np.random.default_rng(7)
        dots = VGroup()
        for i in range(18):
            x = 0.55 + i * 0.38
            y = 5.0 - 0.42 * x + rng.normal(0, 0.14)
            dots.add(Dot(axes.coords_to_point(x, y), color=SUBQ_BLUE, radius=0.055))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.05), run_time=PACE_SLOW)

        law = axes.plot(lambda x: 5.0 - 0.42 * x, x_range=[0.35, 7.85], color=SUBQ_YELLOW, stroke_width=3.5)
        self.play(Create(law), run_time=PACE_SLOW)

        eq = text_equation("L(N) ≈ (N_c / N)^α", color=SUBQ_FG).scale(0.78).to_edge(RIGHT, buff=0.45).shift(UP * 0.8)
        self.play(Write(eq), run_time=PACE_NORMAL)

        bridge = body("Scaling laws fund bigger models — not cheaper attention.", color=SUBQ_MUTED).scale(0.62)
        bridge.to_edge(DOWN, buff=0.65)
        self.play(FadeIn(bridge, shift=UP * 0.1), run_time=PACE_NORMAL)
        self.wait(2.0)
