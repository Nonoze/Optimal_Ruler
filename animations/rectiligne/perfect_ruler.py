from manim import *


class Tableau(Scene):
	def build_blank_ruler(self, L):
		length_scene = 10
		left = LEFT * (length_scene / 2)
		right = RIGHT * (length_scene / 2)
		ruler = Line(left, right, stroke_width=4)

		def x_to_point(x):
			return ruler.point_from_proportion(x / L)

		mini_ticks = VGroup()
		for x in range(L + 1):
			p = x_to_point(x)
			tick = Line(
				p + UP * 0.12,
				p + DOWN * 0.12,
				color=GRAY,
				stroke_width=2,
				stroke_opacity=0.75,
			)
			mini_ticks.add(tick)

		return ruler, mini_ticks, x_to_point

	def draw_case(self, increments, conflict_mode):
		L = 10

		ruler, mini_ticks, x_to_point = self.build_blank_ruler(L)
		self.play(Create(ruler), run_time=1.0)

		marks = [0]
		for d in increments:
			marks.append(marks[-1] + d)

		main_ticks = VGroup()
		main_labels = VGroup()
		step_labels = VGroup()

		p0 = x_to_point(0)
		t0 = Line(p0 + UP * 0.23, p0 + DOWN * 0.23, color=WHITE, stroke_width=5)
		l0 = Text("0", font_size=24).next_to(p0, DOWN, buff=0.25)
		main_ticks.add(t0)
		main_labels.add(l0)
		self.play(FadeIn(mini_ticks), Create(t0), FadeIn(l0), run_time=0.4)

		for i, d in enumerate(increments):
			a = marks[i]
			b = marks[i + 1]
			pa = x_to_point(a)
			pb = x_to_point(b)

			seg = Line(pa, pb, color=BLUE, stroke_width=7)
			tick_b = Line(pb + UP * 0.23, pb + DOWN * 0.23, color=WHITE, stroke_width=5)
			label_b = Text(str(b), font_size=24).next_to(pb, DOWN, buff=0.25)
			step_lab = MathTex(rf"d_{{{i+1}}}={d}", font_size=30, color=YELLOW).next_to(seg, UP, buff=0.15).shift(UP * 0.1)

			main_ticks.add(tick_b)
			main_labels.add(label_b)
			step_labels.add(step_lab)
			self.play(Create(seg), Create(tick_b), FadeIn(label_b), FadeIn(step_lab), run_time=0.6)
			self.wait(0.2)
			self.play(FadeOut(seg), run_time=0.2)

		if conflict_mode == 1:
			# Distance de 0 a 3 vaut 3, deja presente avec +3.
			brace_a = BraceBetweenPoints(
				x_to_point(0) + DOWN * 0.35,
				x_to_point(3) + DOWN * 0.35,
				direction=DOWN,
				color=RED,
			)
			brace_b = BraceBetweenPoints(
				x_to_point(3) + DOWN * 0.35,
				x_to_point(6) + DOWN * 0.35,
				direction=DOWN,
				color=ORANGE,
			)
			lab_a = MathTex(r"1+2=3", font_size=31, color=RED).next_to(brace_a, DOWN, buff=0.12)
			lab_b = MathTex(r"3", font_size=31, color=ORANGE).next_to(brace_b, DOWN, buff=0.12)
			self.play(Create(brace_a), FadeIn(lab_a), run_time=0.8)
			self.play(Create(brace_b), FadeIn(lab_b), run_time=0.8)
			self.wait(0.3)
		elif conflict_mode == 2:
			# 1 + 3 = 4, qui existe deja comme distance.
			brace_a = BraceBetweenPoints(
				x_to_point(0) + DOWN * 0.35,
				x_to_point(4) + DOWN * 0.35,
				direction=DOWN,
				color=RED,
			)
			brace_b = BraceBetweenPoints(
				x_to_point(6) + DOWN * 0.35,
				x_to_point(10) + DOWN * 0.35,
				direction=DOWN,
				color=ORANGE,
			)
			lab_a = MathTex(r"1+3=4", font_size=31, color=RED).next_to(brace_a, DOWN, buff=0.12)
			lab_b = MathTex(r"4", font_size=31, color=ORANGE).next_to(brace_b, DOWN, buff=0.12)
			self.play(Create(brace_a), FadeIn(lab_a), run_time=0.8)
			self.play(Create(brace_b), FadeIn(lab_b), run_time=0.8)
			self.wait(0.3)
		elif conflict_mode == 3:
			# 1 + 4 = 5, distance nouvelle (pas dans {1,2,3,4}).
			brace_a = BraceBetweenPoints(
				x_to_point(0) + DOWN * 0.35,
				x_to_point(5) + DOWN * 0.35,
				direction=DOWN,
				color=GREEN,
			)
			lab_a = MathTex(r"1+4=5", font_size=32, color=GREEN).next_to(brace_a, DOWN, buff=0.12)
			lab_b = MathTex(r"5\notin\{1,2,3,4\}", font_size=31, color=GREEN).next_to(lab_a, RIGHT, buff=0.8)
			self.play(Create(brace_a), FadeIn(lab_a), run_time=0.9)
			self.play(FadeIn(lab_b), run_time=0.5)
			self.wait(0.3)
		else:
			brace_a = BraceBetweenPoints(
				x_to_point(5) + DOWN * 0.35,
				x_to_point(10) + DOWN * 0.35,
				direction=DOWN,
				color=RED,
			)
			brace_b = BraceBetweenPoints(
				x_to_point(0) + DOWN * 0.35,
				x_to_point(5) + DOWN * 0.35,
				direction=DOWN,
				color=ORANGE,
			)
			lab_a = MathTex(r"2+3=5", font_size=31, color=RED).next_to(brace_a, DOWN, buff=0.12)
			lab_b = MathTex(r"1+4=5", font_size=31, color=ORANGE).next_to(brace_b, DOWN, buff=0.12)
			self.play(Create(brace_a), FadeIn(lab_a), run_time=0.8)
			self.play(Create(brace_b), FadeIn(lab_b), run_time=0.8)
			self.wait(0.3)

		self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

	def construct(self):
		self.draw_case(
			[1, 2, 3, 4],
			1,
		)

		self.draw_case(
			[1, 3, 2, 4],
			2,
		)

		self.draw_case(
			[1, 4, 2, 3],
			3,
		)

		self.draw_case(
			[1, 4, 2, 3],
			4,
		)