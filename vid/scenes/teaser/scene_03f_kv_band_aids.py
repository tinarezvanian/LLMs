"""Teaser scene 3f — KV cache mitigations: MHA vs GQA vs MQA; FlashAttention caveat.

Book tie-in: KV cache chapter — engineering reduces bytes, not n² FLOPs (docs/scaling_attention).
"""

from manim import *

from vid.theme import (
    apply_dark_theme,
    body,
    caption,
    heading,
    mono,
    SUBQ_FG,
    SUBQ_MUTED,
    SUBQ_BLUE,
    SUBQ_YELLOW,
    SUBQ_GREEN,
    PACE_NORMAL,
    PACE_SLOW,
)


class Scene03FKVBandAids(Scene):
    def construct(self):
        apply_dark_theme(self)

        title = heading("Engineering shrinks the KV bill", color=SUBQ_FG).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=PACE_NORMAL)

        def bar(label: str, frac: float, color: str) -> VGroup:
            w = 4.2
            h = 0.55
            outline = Rectangle(width=w, height=h, stroke_color=SUBQ_FG, stroke_width=2)
            fill = Rectangle(width=w * frac, height=h - 0.06, stroke_width=0, fill_color=color, fill_opacity=0.88)
            fill.align_to(outline, LEFT).align_to(outline, UP).shift(DOWN * 0.02 + RIGHT * 0.02)
            lab = mono(label, color=SUBQ_FG, size=22).next_to(outline, UP, buff=0.12)
            return VGroup(lab, outline, fill)

        b_mha = bar("MHA — full KV per head", 1.0, SUBQ_BLUE).shift(UP * 0.85)
        b_gqa = bar("GQA — shared KV per group", 0.35, SUBQ_YELLOW).next_to(b_mha, DOWN, buff=0.65)
        b_mqa = bar("MQA — one KV for all heads", 0.12, SUBQ_GREEN).next_to(b_gqa, DOWN, buff=0.65)

        self.play(FadeIn(b_mha, shift=DOWN * 0.1), run_time=PACE_NORMAL)
        self.play(FadeIn(b_gqa, shift=DOWN * 0.1), run_time=PACE_NORMAL)
        self.play(FadeIn(b_mqa, shift=DOWN * 0.1), run_time=PACE_SLOW)
        self.wait(0.45)

        fa = caption(
            "FlashAttention: fewer materialised n×n activations — same asymptotic attention FLOPs.",
            color=SUBQ_MUTED,
        ).scale(0.92).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(fa, shift=UP * 0.1), run_time=PACE_SLOW)
        self.wait(2.0)
