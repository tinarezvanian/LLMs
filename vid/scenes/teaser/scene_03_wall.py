"""Teaser scene 3 — the KV cache wall. 524 GB overflows an H100."""

from manim import *
from manim.utils.rate_functions import smooth

from vid.theme import apply_dark_theme, body, caption, SUBQ_FG, SUBQ_RED, SUBQ_MUTED, PACE_NORMAL, PACE_SLOW
from vid.lib.mobjects import GPUOutline, KVCacheBar


def _fraction_from_tokens(tokens: float) -> float:
    """Smooth KV fill vs token count (piecewise linear through smoke-test keyframes)."""
    t = float(tokens)
    if t <= 100_000:
        return max(0.05, 0.1 * (t / 100_000.0))
    if t <= 500_000:
        u = (t - 100_000.0) / (500_000.0 - 100_000.0)
        return 0.1 + u * (0.5 - 0.1)
    if t <= 1_000_000:
        u = (t - 500_000.0) / (1_000_000.0 - 500_000.0)
        return 0.5 + u * (6.5 - 0.5)
    return 6.5


class Scene03Wall(Scene):
    def construct(self):
        apply_dark_theme(self)

        gpu = GPUOutline(label="H100   80 GB").to_edge(LEFT, buff=1.5)

        tracker = ValueTracker(100_000.0)

        def make_bar() -> KVCacheBar:
            tok = int(tracker.get_value())
            return KVCacheBar(
                fraction=_fraction_from_tokens(tracker.get_value()),
                label=f"KV cache @ {tok:,} tokens",
            ).to_edge(RIGHT, buff=1.5)

        bar = always_redraw(make_bar)

        self.play(FadeIn(gpu), FadeIn(bar), run_time=PACE_NORMAL)
        self.wait(0.35)

        self.play(tracker.animate.set_value(500_000.0), run_time=1.8, rate_func=smooth)
        self.wait(0.35)
        self.play(tracker.animate.set_value(1_000_000.0), run_time=2.0, rate_func=smooth)

        callout = body("524 GB", color=SUBQ_RED).scale(1.5).next_to(bar, UP, buff=0.6)
        cap = caption("on a card with 80", color=SUBQ_MUTED).next_to(callout, DOWN, buff=0.1)
        self.play(FadeIn(callout, shift=DOWN * 0.2), FadeIn(cap), run_time=PACE_NORMAL)
        self.wait(1.0)
