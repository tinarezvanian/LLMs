"""Deep-dive scene 11 — SubQ benchmark callouts, with sources cited."""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    source_footnote,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_MUTED,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene11Benchmarks(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("what they claim", color=SUBQ_FG).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        rows = [
            ("12,000,000", "tokens of context (research)"),
            ("1,000,000", "tokens in production API"),
            ("52x", "faster than FlashAttention at 1M tokens"),
            ("1000x", "less attention compute at 12M tokens"),
            ("95%", "accuracy on RULER 128K"),
        ]

        items = VGroup()
        for stat, desc in rows:
            stat_t = body(stat, color=SUBQ_GREEN).scale(1.1)
            desc_t = caption(desc, color=SUBQ_FG).scale(0.9)
            row = VGroup(stat_t, desc_t).arrange(RIGHT, buff=0.5)
            items.add(row)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        items.move_to(ORIGIN).shift(DOWN * 0.2)

        for row in items:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=PACE_SLOW * 0.5)

        cite = source_footnote(
            "Source: subq.ai/introducing-subq, May 5 2026. Independent verification pending."
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cite), run_time=PACE_NORMAL)
        self.wait(2.0)
