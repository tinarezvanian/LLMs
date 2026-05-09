"""Deep-dive scene 4 — Chinchilla isoflops valley.

Conceptually shows the 20:1 token-to-param sweet spot. Implemented as a 2D loss surface
slice rather than full 3D — much faster to render, just as readable for video.
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    heading,
    caption,
    equation,
    source_footnote,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_YELLOW,
    SUBQ_MUTED,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene04Chinchilla(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Chinchilla (Hoffmann et al., 2022)", color=SUBQ_FG).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        )
        x_label = caption("log10(D / N)   tokens-per-parameter ratio", color=SUBQ_MUTED).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = caption("loss at fixed compute", color=SUBQ_MUTED).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI / 2)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=PACE_NORMAL)

        valley = axes.plot(lambda x: 0.4 * (x - 3.0) ** 2 + 1.0, x_range=[0.2, 5.8], color=SUBQ_YELLOW, stroke_width=4)
        self.play(Create(valley), run_time=PACE_SLOW)

        marker = Dot(axes.c2p(3.0, 1.0), color=SUBQ_GREEN, radius=0.1)
        marker_label = body("D ~ 20 N", color=SUBQ_GREEN).scale(0.6).next_to(marker, UP, buff=0.2)
        self.play(FadeIn(marker, scale=0.5), Write(marker_label), run_time=PACE_NORMAL)

        src = source_footnote("Hoffmann et al., arXiv:2203.15556 (2022)").to_edge(DOWN, buff=0.3).shift(RIGHT * 3)
        self.play(FadeIn(src), run_time=PACE_NORMAL)
        self.wait(2.0)
