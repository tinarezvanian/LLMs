"""Teaser scene 5 — payoff. Whole repo, whole book, whole video flow into one prompt."""

from manim import *

from vid.theme import apply_dark_theme, body, SUBQ_FG, SUBQ_GREEN, SUBQ_MUTED, PACE_NORMAL, PACE_SLOW


class Scene05Payoff(Scene):
    def construct(self):
        apply_dark_theme(self)

        prompt_box = RoundedRectangle(corner_radius=0.2, height=2.5, width=5.0, stroke_color=SUBQ_GREEN, stroke_width=3)
        prompt_label = body("one prompt", color=SUBQ_GREEN).move_to(prompt_box.get_center())
        prompt_group = VGroup(prompt_box, prompt_label).to_edge(RIGHT, buff=1.5)

        items = []
        for i, label in enumerate(["whole codebase", "500-page PDF", "video archive"]):
            chip = RoundedRectangle(corner_radius=0.15, height=0.7, width=3.0, stroke_color=SUBQ_FG, stroke_width=2)
            txt = body(label, color=SUBQ_FG).scale(0.6).move_to(chip.get_center())
            grp = VGroup(chip, txt)
            grp.to_edge(LEFT, buff=1.0).shift(UP * (1.5 - i * 1.2))
            items.append(grp)

        self.play(*[FadeIn(it, shift=RIGHT * 0.3) for it in items], FadeIn(prompt_group), run_time=PACE_NORMAL)
        self.wait(0.4)

        for it in items:
            arrow = Arrow(it.get_right(), prompt_group.get_left(), buff=0.2, stroke_color=SUBQ_GREEN)
            self.play(GrowArrow(arrow), it.animate.shift(RIGHT * 0.5), run_time=PACE_NORMAL * 0.8)
        self.wait(1.0)
