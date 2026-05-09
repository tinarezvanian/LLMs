"""Deep-dive scene 10 — where SubQ fits on the post-transformer tree."""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_MUTED,
    PACE_NORMAL,
    PACE_SLOW,
)
from vid.lib.mobjects import PostTransformerTree, SubQWordmark


class Scene10SubQPosition(Scene):
    def construct(self):
        apply_dark_theme(self)

        tree = PostTransformerTree().scale(0.85).shift(UP * 0.5)
        self.play(FadeIn(tree), run_time=PACE_NORMAL)
        self.wait(0.3)

        subq_node, subq_line = tree.branches[-1]
        ring = Circle(radius=1.1, stroke_color=SUBQ_GREEN, stroke_width=4).move_to(subq_node.get_center())
        self.play(Create(ring), Flash(subq_node, color=SUBQ_GREEN, line_length=0.4), run_time=PACE_SLOW)

        wordmark = SubQWordmark(scale=0.7).to_edge(DOWN, buff=1.5)
        tagline = body("subquadratic sparse attention  -  proprietary internals", color=SUBQ_MUTED).scale(0.55)
        tagline.next_to(wordmark, DOWN, buff=0.3)
        self.play(FadeIn(wordmark, shift=DOWN * 0.2), FadeIn(tagline), run_time=PACE_NORMAL)
        self.wait(1.5)
