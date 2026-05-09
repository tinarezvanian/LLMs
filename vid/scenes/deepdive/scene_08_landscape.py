"""Deep-dive scene 8 — the post-transformer tree. SSMs, convs, linear attention, hybrids."""

from manim import *

from vid.theme import apply_dark_theme, heading, SUBQ_FG, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import PostTransformerTree


class Scene08Landscape(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("the post-transformer landscape", color=SUBQ_FG).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        tree = PostTransformerTree().shift(DOWN * 0.3)
        self.play(FadeIn(tree.root), run_time=PACE_NORMAL)

        for node, line in tree.branches:
            self.play(Create(line), FadeIn(node, shift=DOWN * 0.1), run_time=PACE_SLOW * 0.6)
        self.wait(1.0)
