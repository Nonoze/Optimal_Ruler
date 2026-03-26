from manim import *
import math
import numpy as np


def read_rulers_from_csv(path):
    rulers = []
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    i = 0
    while i < len(lines):
        L = int(lines[i])
        i += 1
        marks = list(map(int, lines[i].split()))
        i += 1
        rulers.append((L, marks))

    return rulers


class CircularRuler(Scene):
    def construct(self):
        csv_path = "ruler_list.csv"
        rulers = read_rulers_from_csv(csv_path)

        for L, marks in rulers:
            self.show_circular_ruler(L, marks)
            self.play(*[FadeOut(mob) for mob in self.mobjects])
            self.wait(0.5)

    def show_circular_ruler(self, L, marks):

        # démonstration d'une règle circulaire de longueur L avec des marques données

        title = MathTex(r"\text{Règle circulaire de longueur } " + str(L), font_size=40).to_edge(UP, buff=0.8).shift(UP*0.2)
        self.play(Write(title))

        radius = 2.5
        circle = Circle(radius=radius).shift(DOWN * 0.5)
        self.play(Create(circle))

        # Conversion position -> point sur le cercle
        def x_to_point(x):
            theta = TAU * (x / L)
            return radius * np.cos(theta) * RIGHT + radius * np.sin(theta) * UP

        def x_to_angle(x):
            return TAU * (x / L)

        # Marques et labels
        tick_length = 0.2
        ticks = VGroup()
        labels = VGroup()

        for i in range(L):
            if i in marks:
                continue

            p = x_to_point(i)
            direction = p / np.linalg.norm(p)
            tick_start = p + direction * tick_length
            tick_end = p - direction * tick_length
            tick = Line(tick_start, tick_end, stroke_width=2, color=GREY).shift(DOWN * 0.5)
            ticks.add(tick)

        for m in marks:
            if (m>=L):
                continue
            p = x_to_point(m)
            # CORRECTION: direction normalisée directement
            direction = p / np.linalg.norm(p)
            tick_start = p + direction * tick_length
            tick_end = p - direction * tick_length
            tick = Line(tick_start, tick_end).shift(DOWN * 0.5)
            ticks.add(tick)

            label_pos = p + direction * 0.4
            label = Text(str(m), font_size=28)
            label.move_to(label_pos).shift(DOWN * 0.5)
            labels.add(label)

        self.play(Create(ticks), Write(labels))
        self.wait(0.5)

        # Segments déjà vus (en gris)
        all_segments = VGroup()

        for d in range(1, L + 1):
            pair = None
            for i in range(len(marks)):
                for j in range(i + 1, len(marks)):
                    if marks[j] - marks[i] == d or L-(marks[j] - marks[i]) == d:
                        if (marks[j] - marks[i] == d):
                            pair = (marks[i], marks[j])
                        else:
                            pair = (marks[j], marks[i])
                        break
                if pair:
                    break

            if d==L:
                pair = (1, 1)
            
            if pair is None:
                continue

            a, b = pair
            angle_a = x_to_angle(a)
            angle_b = x_to_angle(b)
            arc_angle = angle_b - angle_a
            if arc_angle < 0:
                arc_angle += TAU

            if angle_a == angle_b:
                arc_angle = TAU
            arc = Arc(
                radius=radius,
                start_angle=angle_a,
                angle=arc_angle,
                color=YELLOW,
                stroke_width=6
            ).shift(DOWN * 0.5)
            
            # Label au milieu de l'arc
            mid_angle = angle_a + arc_angle / 2
            label_pos = radius * 1.2 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
            d_label = MathTex(str(d), font_size=34).move_to(label_pos).shift(DOWN * 0.5)

            self.play(Create(arc), FadeIn(d_label))
            self.wait(0.5)

            self.play(
                FadeOut(arc),
                FadeOut(d_label),
            )

        self.wait(1)