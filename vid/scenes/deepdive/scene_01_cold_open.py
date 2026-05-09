"""Deep-dive scene 1 — cold open. Filled in post with screen capture footage.

This scene is a placeholder: the actual visual is screen-recorded SubQ Code
loading a 400k-token codebase, intercut with a competing tool OOM-erroring.
Manim is only needed for an end-of-scene title card.
"""

from manim import *

from vid.theme import apply_dark_theme, body, SUBQ_FG, SUBQ_MUTED, PACE_NORMAL


class Scene01ColdOpenTitle(Scene):
    def construct(self):
        apply_dark_theme(self)
        title_a = body("400,000 tokens. One prompt.", color=SUBQ_FG).scale(1.2)
        title_b = body("Same machine. Different model.", color=SUBQ_MUTED).scale(0.7)
        title_b.next_to(title_a, DOWN, buff=0.5)
        self.play(FadeIn(title_a, shift=UP * 0.2), run_time=PACE_NORMAL)
        self.play(FadeIn(title_b), run_time=PACE_NORMAL)
        self.wait(1.5)
