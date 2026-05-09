"""Teaser scene 4 — the break. Red curve cracks; green linear curve replaces it."""

import numpy as np
from manim import *
from manim.utils.rate_functions import smooth

from vid.theme import apply_dark_theme, body, SUBQ_GREEN, SUBQ_RED, PACE_FAST, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import ScalingCurve, SubQWordmark


class Scene04Break(Scene):
    def construct(self):
        apply_dark_theme(self)

        red = ScalingCurve(kind="quadratic", color=SUBQ_RED)
        green = ScalingCurve(kind="linear", color=SUBQ_GREEN)
        self.add(red)
        self.wait(0.25)

        # "Crack" shards along the quadratic stroke — cheap particle read.
        shards = VGroup()
        for i in range(1, 18):
            p = red.graph.point_from_proportion(i / 18.0)
            angle = PI / 4 + (i % 3) * PI / 9
            d = 0.12 * np.array([np.cos(angle), np.sin(angle), 0.0])
            shard = Line(p - d, p + d, stroke_width=2.5, color=SUBQ_RED)
            shard.set_opacity(0.9)
            shards.add(shard)

        self.play(
            LaggedStart(*[FadeIn(s, scale=0.2) for s in shards], lag_ratio=0.03, run_time=PACE_FAST * 1.2),
            red.graph.animate.set_stroke(opacity=0.25),
            run_time=PACE_NORMAL,
        )
        self.play(Create(green.graph), run_time=PACE_SLOW, rate_func=smooth)
        self.play(FadeOut(red), FadeOut(shards), run_time=PACE_NORMAL)

        wordmark = SubQWordmark(scale=0.9).to_edge(DOWN, buff=1.0)
        tagline = body("1M prod · 12M research · 52× vs FA @ 1M", color=SUBQ_GREEN).next_to(wordmark, UP, buff=0.4).scale(0.65)
        self.play(FadeIn(wordmark, shift=UP * 0.2), FadeIn(tagline), run_time=PACE_NORMAL)
        self.wait(1.0)
