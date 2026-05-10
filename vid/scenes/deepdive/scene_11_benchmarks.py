"""Deep-dive scene 11 — benchmark callouts + MRCR v2 leaderboard (honest framing).

SubQ in the conversation, not necessarily at the top. Source footnote per TASK 4.11.
"""

from __future__ import annotations

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    mono,
    source_footnote,
    SUBQ_FG,
    SUBQ_GREEN,
    SUBQ_MUTED,
    SUBQ_CYAN,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene11Benchmarks(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("benchmarks — honest framing", color=SUBQ_FG).to_edge(UP, buff=0.55).scale(0.92)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=PACE_NORMAL)

        intro = caption("launch claims + long-context eval", color=SUBQ_MUTED).scale(0.85).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(intro), run_time=PACE_NORMAL)

        rows = [
            ("12,000,000", "tokens — research context window"),
            ("1,000,000", "tokens — production API"),
            ("52×", "prefill vs FlashAttention-2 @ 1M (B200)"),
            ("95%", "RULER @ 128K (avg of 13 tasks)"),
        ]
        stats = VGroup()
        for stat, desc in rows:
            stat_t = body(stat, color=SUBQ_GREEN).scale(0.95)
            desc_t = caption(desc, color=SUBQ_FG).scale(0.82)
            row = VGroup(stat_t, desc_t).arrange(RIGHT, buff=0.45)
            stats.add(row)
        stats.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        stats.next_to(intro, DOWN, buff=0.45).shift(LEFT * 0.2)

        for row in stats:
            self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=PACE_SLOW * 0.45)

        hdr = heading("MRCR v2 leaderboard", color=SUBQ_FG).scale(0.58).next_to(stats, DOWN, buff=0.55)
        sub = caption("multi-hop reasoning over fragmented evidence", color=SUBQ_MUTED).scale(0.78)
        sub.next_to(hdr, DOWN, buff=0.12)
        self.play(FadeIn(hdr), FadeIn(sub), run_time=PACE_NORMAL)

        leaderboard_lines = [
            ("Opus 4.6", "78.3%", False),
            ("GPT 5.5", "74.0%", False),
            ("SSA / SubQ", "65.9%", True),
            ("GPT 5.4", "36.6%", False),
            ("Opus 4.7", "32.2%", False),
            ("Gemini 3.1 Pro", "26.3%", False),
        ]
        table_rows = VGroup()
        for name, pct, highlight in leaderboard_lines:
            name_c = SUBQ_CYAN if highlight else SUBQ_FG
            pct_c = SUBQ_GREEN if highlight else SUBQ_FG
            left = mono(name, color=name_c, size=26)
            right = mono(pct, color=pct_c, size=26)
            inner = VGroup(left, right).arrange(RIGHT, buff=2.9)
            if highlight:
                rect = SurroundingRectangle(inner, color=SUBQ_GREEN, buff=0.14, stroke_width=2)
                inner = VGroup(rect, inner)
            table_rows.add(inner)

        table_rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.28)
        table_rows.next_to(sub, DOWN, buff=0.35)

        col_hdr = VGroup(
            mono("Model", color=SUBQ_MUTED, size=22),
            mono("MRCR v2", color=SUBQ_MUTED, size=22),
        ).arrange(RIGHT, buff=3.35)
        col_hdr.next_to(table_rows, UP, buff=0.18, aligned_edge=RIGHT)

        self.play(FadeIn(col_hdr), LaggedStart(*[FadeIn(r) for r in table_rows], lag_ratio=0.12), run_time=PACE_SLOW)

        cite = source_footnote(
            "Source: subq.ai/how-ssa-makes-long-context-practical, May 5 2026. "
            "SubQ states benchmarks are third-party verified; full model card pending."
        ).scale(0.78).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(cite), run_time=PACE_NORMAL)
        self.wait(2.0)
