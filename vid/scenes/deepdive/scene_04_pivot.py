"""Deep-dive scene 4 — the pivot. Scaling line extends, then context length kills it."""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_GREEN,
    SUBQ_RED,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene04Pivot(Scene):
    def construct(self):
        apply_dark_theme(self)

        good_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=3.5,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        ).to_edge(UP, buff=1.0)
        good_line = good_axes.plot(lambda x: 4.5 - 0.45 * x, x_range=[0.3, 7.8], color=SUBQ_GREEN, stroke_width=4)
        good_label = caption("loss vs scale (smooth, predictable)", color=SUBQ_MUTED).next_to(good_axes, DOWN, buff=0.2)
        self.play(Create(good_axes), Create(good_line), FadeIn(good_label), run_time=PACE_NORMAL)

        bad_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=3.5,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        ).to_edge(DOWN, buff=0.6)
        bad_curve = bad_axes.plot(lambda x: min(0.08 * x * x, 5.5), x_range=[0.3, 7.8], color=SUBQ_RED, stroke_width=4)
        bad_label = caption("compute vs context length n  (n^2)", color=SUBQ_RED).next_to(bad_axes, DOWN, buff=0.2)
        self.play(Create(bad_axes), Create(bad_curve), FadeIn(bad_label), run_time=PACE_SLOW)

        kicker = body("scaling laws don't tell you what context length costs", color=SUBQ_FG).scale(0.7)
        kicker.next_to(bad_label, DOWN, buff=0.4)
        self.play(FadeIn(kicker, shift=UP * 0.1), run_time=PACE_NORMAL)
        self.wait(1.5)
