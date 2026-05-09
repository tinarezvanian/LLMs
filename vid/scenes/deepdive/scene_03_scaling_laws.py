"""Deep-dive scene 3 — scaling laws. Kaplan plot + Chinchilla isoflops valley."""

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
    SUBQ_GREEN,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene03ScalingLaws(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Scaling laws (Kaplan et al. 2020)", color=SUBQ_FG).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=4.5,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        ).shift(DOWN * 0.5)
        x_label = caption("log(parameters N)", color=SUBQ_MUTED).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = caption("log(loss L)", color=SUBQ_MUTED).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI / 2)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=PACE_NORMAL)

        rng = np.random.default_rng(42)
        dots = VGroup()
        for i in range(20):
            x = 0.5 + i * 0.35
            y = 5.0 - 0.45 * x + rng.normal(0, 0.18)
            dot = Dot(axes.coords_to_point(x, y), color=SUBQ_BLUE, radius=0.06)
            dots.add(dot)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.04), run_time=PACE_SLOW)

        line = axes.plot(lambda x: 5.0 - 0.45 * x, x_range=[0.3, 7.8], color=SUBQ_YELLOW, stroke_width=4)
        self.play(Create(line), run_time=PACE_SLOW)

        eq = text_equation("L(N) = (N_c / N)^0.076", color=SUBQ_FG).scale(0.9)
        eq.to_edge(RIGHT, buff=0.7).shift(UP * 1.5)
        self.play(Write(eq), run_time=PACE_NORMAL)
        self.wait(1.0)

        chinchilla = caption(
            "Chinchilla 2022 correction: D ~ 20 x N at compute-optimal", color=SUBQ_GREEN
        ).next_to(axes, DOWN, buff=0.6)
        self.play(FadeIn(chinchilla, shift=UP * 0.2), run_time=PACE_NORMAL)
        self.wait(1.5)
