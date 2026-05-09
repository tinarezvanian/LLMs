"""Deep-dive scene 12 — title card transitioning into the live SubQ Code demo."""

from manim import *

from vid.theme import apply_dark_theme, body, heading, SUBQ_FG, SUBQ_GREEN, SUBQ_MUTED, PACE_NORMAL


class Scene12DemoIntro(Scene):
    def construct(self):
        apply_dark_theme(self)
        title = heading("don't trust me. don't trust them.", color=SUBQ_FG).scale(0.9)
        sub = body("run the benchmark yourself.", color=SUBQ_GREEN).scale(0.8)
        sub.next_to(title, DOWN, buff=0.5)
        repo = body("github.com/tinarezvanian/subq-quickstart", color=SUBQ_MUTED).scale(0.6)
        repo.next_to(sub, DOWN, buff=0.6)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=PACE_NORMAL)
        self.play(FadeIn(sub), run_time=PACE_NORMAL)
        self.play(FadeIn(repo), run_time=PACE_NORMAL)
        self.wait(2.0)
