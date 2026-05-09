"""Deep-dive scene 7 — FlashAttention defense.

Three curves in one frame: standard attention (red, O(n^2)), FlashAttention
(yellow, smaller constant but same asymptote), subquadratic (green, linear).
The kicker is the asymptote — FlashAttention is brilliant but the disease is
still there.

Reconciles two earlier drafts; the linear comparison line is intentional even
though scene 4 also pivots into it — repetition reinforces the contract.
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_MUTED,
    SUBQ_RED,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene07FlashAttention(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("FlashAttention: brilliant, but still O(n^2)", color=SUBQ_FG).scale(0.9).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"stroke_color": SUBQ_MUTED, "stroke_width": 2},
        )
        self.play(Create(axes), run_time=PACE_NORMAL)

        attn = axes.plot(lambda x: min(x * x / 6.0, 6), x_range=[0.1, 6], color=SUBQ_RED, stroke_width=4)
        attn_label = caption("standard attention", color=SUBQ_RED).next_to(attn.get_end(), UP, buff=0.1).scale(0.8)
        self.play(Create(attn), FadeIn(attn_label), run_time=PACE_SLOW)

        flash = axes.plot(lambda x: min(x * x / 18.0, 6), x_range=[0.1, 6], color=SUBQ_YELLOW, stroke_width=4)
        flash_label = caption("FlashAttention (~3x faster, same shape)", color=SUBQ_YELLOW).scale(0.7)
        flash_label.next_to(flash.get_end(), UP, buff=0.6)
        self.play(Create(flash), FadeIn(flash_label), run_time=PACE_SLOW)

        linear = axes.plot(lambda x: 0.6 * x, x_range=[0.1, 6], color=SUBQ_GREEN, stroke_width=4)
        linear_label = caption("subquadratic (linear)", color=SUBQ_GREEN).scale(0.7)
        linear_label.next_to(linear.get_end(), DOWN, buff=0.1)
        self.play(Create(linear), FadeIn(linear_label), run_time=PACE_SLOW)

        x_label = caption("context length n", color=SUBQ_MUTED).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = caption("compute / memory", color=SUBQ_MUTED).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI / 2)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=PACE_NORMAL)

        kicker = body("the asymptote stays", color=SUBQ_FG).scale(0.8).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(kicker, shift=UP * 0.2), run_time=PACE_NORMAL)
        self.wait(1.5)
