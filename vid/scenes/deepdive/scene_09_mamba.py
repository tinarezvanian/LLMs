"""Deep-dive scene 9 — Mamba intuition. A rolling hidden state vs the n x n grid."""

from manim import *
import numpy as np

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_GREEN,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene09Mamba(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = caption("Mamba: a single rolling state, updated per token", color=SUBQ_GREEN).to_edge(UP, buff=0.6)
        self.play(FadeIn(title), run_time=PACE_NORMAL)

        track = Line(LEFT * 5, RIGHT * 5, stroke_color=SUBQ_MUTED, stroke_width=2)
        self.play(Create(track), run_time=PACE_NORMAL)

        n = 7
        tokens = VGroup()
        for i in range(n):
            x = -4.5 + i * 1.5
            t = Square(side_length=0.4, stroke_color=SUBQ_BLUE, fill_color=SUBQ_BLUE, fill_opacity=0.4)
            t.move_to(np.array([x, 0, 0]))
            tokens.add(t)
        self.play(LaggedStartMap(FadeIn, tokens, lag_ratio=0.1), run_time=PACE_NORMAL)

        state = Circle(radius=0.5, stroke_color=SUBQ_GREEN, stroke_width=3, fill_color=SUBQ_GREEN, fill_opacity=0.2)
        state.next_to(tokens[0], DOWN, buff=0.7)
        state_label = caption("h_t", color=SUBQ_GREEN).move_to(state.get_center())
        state_grp = VGroup(state, state_label)
        self.play(FadeIn(state_grp), run_time=PACE_NORMAL)

        for i in range(n):
            target = tokens[i].get_center() + DOWN * 0.7
            self.play(
                state_grp.animate.move_to(target),
                tokens[i].animate.set_fill(SUBQ_GREEN, opacity=0.6),
                run_time=0.4,
            )

        eq = (
            VGroup(
                body("h_t = A · h_{t−1} + B · x_t", color=SUBQ_FG).scale(0.72),
                body("y_t = C · h_t", color=SUBQ_FG).scale(0.72),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            .to_edge(DOWN, buff=0.55)
        )
        self.play(LaggedStart(Write(eq[0]), Write(eq[1]), lag_ratio=0.35), run_time=PACE_SLOW)

        complexity = body("O(n)  vs  attention's O(n²)", color=SUBQ_GREEN).scale(0.7).next_to(eq, UP, buff=0.25)
        self.play(FadeIn(complexity), run_time=PACE_NORMAL)
        self.wait(1.5)
