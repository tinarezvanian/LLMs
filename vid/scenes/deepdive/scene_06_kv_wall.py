"""Deep-dive scene 6 — the KV cache wall. 524 GB overflows an 80 GB H100."""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    equation,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_RED,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import GPUOutline, KVCacheBar


class Scene06KVWall(Scene):
    def construct(self):
        apply_dark_theme(self)

        eq = equation(
            r"\text{KV cache} \;=\; 2 \cdot L \cdot H \cdot d_{head} \cdot n \cdot \text{sizeof(fp16)}",
            color=SUBQ_FG,
        ).scale(0.8).to_edge(UP, buff=0.6)
        self.play(Write(eq), run_time=PACE_NORMAL)

        concrete = caption(
            "L=32, H=32, d_head=128, fp16  ->  524 KB / token",
            color=SUBQ_MUTED,
        ).next_to(eq, DOWN, buff=0.3)
        self.play(FadeIn(concrete), run_time=PACE_NORMAL)

        gpu = GPUOutline(label="H100   80 GB").shift(LEFT * 3 + DOWN * 1.0)
        bar = KVCacheBar(fraction=6.5, label="KV cache @ 1M tokens").shift(RIGHT * 1.5 + DOWN * 1.0)
        self.play(FadeIn(gpu), Create(bar), run_time=PACE_SLOW)

        callout = body("524 GB", color=SUBQ_RED).scale(1.4).next_to(bar, UP, buff=0.5)
        self.play(FadeIn(callout, shift=DOWN * 0.2), run_time=PACE_NORMAL)
        self.wait(1.5)
