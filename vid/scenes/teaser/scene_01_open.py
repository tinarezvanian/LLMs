"""Teaser scene 1 — cold open: a clean linear curve, "what we wish AI cost"."""

from manim import *

from vid.theme import apply_dark_theme, body, SUBQ_BLUE, SUBQ_MUTED, PACE_NORMAL
from vid.lib.mobjects import ScalingCurve


class Scene01Open(Scene):
    def construct(self):
        apply_dark_theme(self)

        curve = ScalingCurve(kind="linear", color=SUBQ_BLUE, stroke_width=6)
        label = body("what we wish AI cost", color=SUBQ_MUTED)
        label.next_to(curve, DOWN, buff=0.3)

        self.play(Create(curve), run_time=PACE_NORMAL * 2)
        self.play(FadeIn(label, shift=UP * 0.2), run_time=PACE_NORMAL)
        self.wait(1.0)
