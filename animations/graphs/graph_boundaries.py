import numpy as np
from io import StringIO
from manim import *

with open("data.csv", "r") as f:
    csv_text = f.read()
arr = np.genfromtxt(StringIO(csv_text), delimiter=",", skip_header=1, dtype=int)

length = arr[:, 0]
segment = arr[:, 1] + 1
valid = length > 0
x = length[valid]
fx = segment[valid]

class GraphWithBoundaries(Scene):
    def construct(self):
        x_max = max(x) if len(x) > 0 else 10
        y_max = max(fx) if len(fx) > 0 else 10


        axes = Axes(
            x_range=[0, 239, 30],
            y_range=[0, 29, 5],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True, 'tip_shape': StealthTip}
        ).shift(DOWN*0.4)

        xlabel = MathTex(r"\ell").next_to(axes.x_axis, RIGHT, buff=0.1)
        ylabel = MathTex(r"m(\ell)").next_to(axes.y_axis, LEFT, buff=0.2)
        title = Tex("Nombre de graduations $m(\\ell)$ en fonction de la longueur $\\ell$ avec les bornes", font_size=40).to_edge(UP)

        graph_line = VMobject(stroke_color=BLUE, stroke_width=4)
        points = [axes.coords_to_point(xi, fx[i]) for i, xi in enumerate(x)]
        graph_line.set_points_as_corners(points)

        # boundary 1 = sqrt(2l), boundary 2 = 2sqrt(l)

        boundary1 = axes.plot(lambda l: np.sqrt(2*l), color=RED, stroke_width=2, x_range=[1, 220])
        boundary2 = axes.plot(lambda l: 2*np.sqrt(l), color=RED, stroke_width=2, x_range=[1, 220])

        boundary1_dashed = DashedVMobject(boundary1, num_dashes=50)
        boundary2_dashed = DashedVMobject(boundary2, num_dashes=50)

        # legend

        legend = VGroup(
            VGroup(Line(start=ORIGIN, end=RIGHT * 0.5, color=BLUE, stroke_width=4), MathTex("m(\\ell)")).arrange(RIGHT, buff=0.3),
            VGroup(DashedVMobject(Line(start=ORIGIN, end=RIGHT * 0.5, color=RED, stroke_width=2), num_dashes=4), MathTex("2\\sqrt{\\ell}")).arrange(RIGHT, buff=0.3),
            VGroup(DashedVMobject(Line(start=ORIGIN, end=RIGHT * 0.5, color=RED, stroke_width=2), num_dashes=4), MathTex("\\sqrt{2\\ell}")).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.5).to_corner(UR).shift(DOWN*1)


        # Animations
        self.play(Create(axes), run_time=1.5)
        self.play(Write(xlabel), Write(ylabel), run_time=1)
        self.play(Write(title), run_time=1.2)
        self.play(Create(graph_line), run_time=2.2)
        self.play(Create(boundary1_dashed), Create(boundary2_dashed), run_time=2)
        
        self.play(FadeIn(legend), run_time=0.8)

        self.wait(2)
