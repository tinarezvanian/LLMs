"""Teaser scene 3 — the KV cache wall. 524 GB overflows an H100."""

from manim import *

from vid.theme import apply_dark_theme, body, caption, SUBQ_FG, SUBQ_RED, SUBQ_MUTED, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import GPUOutline, KVCacheBar


class Scene03Wall(Scene):
    def construct(self):
        apply_dark_theme(self)

        gpu = GPUOutline(label="H100   80 GB").to_edge(LEFT, buff=1.5)
        bar = KVCacheBar(fraction=0.1, label="KV cache @ 100k tokens").to_edge(RIGHT, buff=1.5)
        self.play(FadeIn(gpu), Create(bar), run_time=PACE_NORMAL)
        self.wait(0.5)

        bar_500k = KVCacheBar(fraction=0.5, label="KV cache @ 500k tokens").move_to(bar)
        self.play(Transform(bar, bar_500k), run_time=PACE_NORMAL)
        self.wait(0.5)

        bar_1m = KVCacheBar(fraction=6.5, label="KV cache @ 1M tokens").move_to(bar)
        self.play(Transform(bar, bar_1m), run_time=PACE_SLOW)

        callout = body("524 GB", color=SUBQ_RED).scale(1.5).next_to(bar, UP, buff=0.6)
        cap = caption("on a card with 80", color=SUBQ_MUTED).next_to(callout, DOWN, buff=0.1)
        self.play(FadeIn(callout, shift=DOWN * 0.2), FadeIn(cap), run_time=PACE_NORMAL)
        self.wait(1.0)
