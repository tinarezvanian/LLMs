"""Teaser scene 5 — payoff. Whole repo, whole book, whole video flow into one prompt."""

from manim import *
from manim.utils.rate_functions import smooth

from vid.theme import apply_dark_theme, body, SUBQ_FG, SUBQ_GREEN, SUBQ_MUTED, SUBQ_YELLOW, PACE_NORMAL, PACE_SLOW


def _icon_code(color: str) -> VGroup:
    bracket_l = Text("{", font_size=44, color=color, weight=BOLD)
    bracket_r = Text("}", font_size=44, color=color, weight=BOLD)
    mid = body("code", color=color).scale(0.45)
    g = VGroup(bracket_l, mid, bracket_r).arrange(RIGHT, buff=0.05)
    box = SurroundingRectangle(g, color=SUBQ_FG, buff=0.12, corner_radius=0.1, stroke_width=2)
    return VGroup(box, g)


def _icon_doc(color: str) -> VGroup:
    page = RoundedRectangle(corner_radius=0.06, height=0.85, width=0.65, stroke_color=color, stroke_width=2)
    lines = VGroup(*[Line(LEFT * 0.2, RIGHT * 0.2, stroke_width=2, color=SUBQ_MUTED) for _ in range(3)])
    lines.arrange(DOWN, buff=0.12).move_to(page.get_center() + UP * 0.08)
    return VGroup(page, lines)


def _icon_film(color: str) -> VGroup:
    frames = VGroup(*[Rectangle(height=0.35, width=0.22, stroke_color=color, stroke_width=2) for _ in range(3)])
    frames.arrange(RIGHT, buff=0.06)
    return frames


class Scene05Payoff(Scene):
    def construct(self):
        apply_dark_theme(self)

        prompt_box = RoundedRectangle(corner_radius=0.2, height=2.5, width=5.0, stroke_color=SUBQ_GREEN, stroke_width=3)
        prompt_label = body("one prompt", color=SUBQ_GREEN).move_to(prompt_box.get_center())
        prompt_group = VGroup(prompt_box, prompt_label).to_edge(RIGHT, buff=1.5)

        rows = [
            ("whole codebase", _icon_code(SUBQ_GREEN)),
            ("500-page PDF", _icon_doc(SUBQ_FG)),
            ("video archive", _icon_film(SUBQ_YELLOW)),
        ]

        items = []
        for i, (label, icon) in enumerate(rows):
            chip = RoundedRectangle(corner_radius=0.15, height=0.95, width=3.4, stroke_color=SUBQ_FG, stroke_width=2)
            txt = body(label, color=SUBQ_FG).scale(0.58).next_to(chip.get_left(), RIGHT, buff=0.35).align_to(chip, UP).shift(DOWN * 0.18)
            ic = icon.scale(0.55).next_to(txt, LEFT, buff=0.25).align_to(txt, UP)
            grp = VGroup(chip, ic, txt)
            grp.to_edge(LEFT, buff=1.0).shift(UP * (1.35 - i * 1.25))
            items.append(grp)

        self.play(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], FadeIn(prompt_group), run_time=PACE_NORMAL)
        self.wait(0.35)

        for it in items:
            arrow = Arrow(it.get_right(), prompt_group.get_left(), buff=0.15, stroke_color=SUBQ_GREEN)
            self.play(GrowArrow(arrow), it.animate.shift(RIGHT * 0.35), run_time=PACE_NORMAL * 0.85, rate_func=smooth)
        self.wait(1.0)
