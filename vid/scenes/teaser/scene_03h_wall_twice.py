"""Teaser scene 3h — training vs inference: two different cost functions.

Book tie-in: what scaling laws omit + inference economics (docs/scaling_attention).
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene03HWallTwice(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Two budgets, one architecture", color=SUBQ_FG).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=PACE_NORMAL)

        col1 = VGroup(
            body("Training", color=SUBQ_BLUE).scale(0.72),
            caption("FLOPs ∝ N · D  (Chinchilla-style token mix)", color=SUBQ_MUTED).scale(0.95),
            caption("Power laws: bigger models predictably drop loss", color=SUBQ_MUTED).scale(0.95),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).shift(LEFT * 2.85 + DOWN * 0.15)

        col2 = VGroup(
            body("Inference", color=SUBQ_YELLOW).scale(0.72),
            caption("Latency + KV footprint per request", color=SUBQ_MUTED).scale(0.95),
            caption("Long context = memory + bandwidth first", color=SUBQ_MUTED).scale(0.95),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).shift(RIGHT * 2.85 + DOWN * 0.15)

        self.play(LaggedStart(FadeIn(col1, shift=RIGHT * 0.12), FadeIn(col2, shift=LEFT * 0.12), lag_ratio=0.35), run_time=PACE_SLOW)
        self.wait(0.45)

        bridge = body(
            "Scaling up N does not, by itself, remove the n² attention tile at decode.",
            color=SUBQ_FG,
        ).scale(0.58).to_edge(DOWN, buff=0.85)
        self.play(FadeIn(bridge, shift=UP * 0.12), run_time=PACE_SLOW)
        self.wait(3.2)
