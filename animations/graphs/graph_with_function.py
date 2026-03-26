import numpy as np
from io import StringIO
from manim import *
from math import sqrt

with open("data.csv", "r") as f:
	csv_text = f.read()
arr = np.genfromtxt(StringIO(csv_text), delimiter=",", skip_header=1, dtype=int)

length = arr[:, 0]
segment = arr[:, 1] + 1
valid = length > 0
x = length[valid]
fx = segment[valid]

def function(l):
	return 1.72*sqrt(l)+0.2

class graph_function(Scene):
	def construct(self):
		x_max = max(x) if len(x) > 0 else 10
		y_max = max(fx) if len(fx) > 0 else 10


		axes = Axes(
			x_range=[0, 239, 30],
			y_range=[0, 29, 5],
			x_length=8,
			y_length=5,
			axis_config={"include_numbers": True, 'tip_shape': StealthTip},
		).shift(LEFT*0)

		xlabel = MathTex(r"\ell").next_to(axes.x_axis, RIGHT, buff=0.1)
		ylabel = MathTex(r"m(\ell)").next_to(axes.y_axis, LEFT, buff=0.2)
		title = Tex("Fonction se rapprochant de $m(\\ell)$", font_size=40).to_edge(UP)

		graph_line = VMobject(stroke_color=BLUE, stroke_width=4)
		points = [axes.coords_to_point(xi, fx[i]) for i, xi in enumerate(x)]
		graph_line.set_points_as_corners(points)

		graph_function = axes.plot(lambda l: function(l), color=ORANGE, stroke_width=4, x_range=[0, 215])

		# residual = VMobject(stroke_color=RED, stroke_width=2)
		# residual_points = [axes.coords_to_point(xi, fx[i] - function(xi)) for i, xi in enumerate(x)]

		# residual.set_points_as_corners(residual_points)

		# legend
		
		legend = VGroup(
			VGroup(Line(start=ORIGIN, end=RIGHT * 0.3, color=BLUE, stroke_width=3), MathTex("m(\\ell)", font_size=36)).arrange(RIGHT, buff=0.23),
			VGroup(Line(start=ORIGIN, end=RIGHT * 0.3, color=ORANGE, stroke_width=3), MathTex("1.72\\sqrt{\\ell}+0.2", font_size=36)).arrange(RIGHT, buff=0.23),
			# VGroup(Line(start=ORIGIN, end=RIGHT * 0.3, color=RED, stroke_width=2), MathTex("m(\\ell) - (1.72\\sqrt{\\ell}+0.2)", font_size=36)).arrange(RIGHT, buff=0.23)
		).arrange(DOWN, buff=0.23, aligned_edge=LEFT).to_corner(UR).shift(DOWN*1).shift(RIGHT*0.2)

		# Animations
		self.play(Create(axes), run_time=1.5)
		self.play(Write(xlabel), Write(ylabel), run_time=1)
		self.play(Write(title), run_time=1.2)
		
		self.play(Create(graph_line), run_time=2.2)
		self.play(Create(graph_function), run_time=2.2)
		# self.play(Create(residual), run_time=2.2)
		
		self.play(FadeIn(legend), run_time=0.8)

		self.wait(2)
