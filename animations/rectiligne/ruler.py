from manim import *

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

class Ruler(Scene):
	def construct(self):
		csv_path = "input.csv"
		rulers = read_rulers_from_csv(csv_path)
		for L, marks in rulers:
			self.show_ruler(L, marks)
			self.play(*[FadeOut(mob) for mob in self.mobjects])
			self.wait(0.5)


	def show_ruler(self, L, marks):

		title = MathTex(
    		r"\text{R\`egle de longueur } \ell=" + str(L) +
    		r"\text{ avec } m(\ell)=" + str(len(marks)) + r"\text{ marques}",
    		font_size=36
		).to_edge(UP, buff=0.8)
		self.play(Write(title))

		length_scene = L - 1
		left = LEFT * (length_scene / 2)
		right = RIGHT * (length_scene / 2)
		ruler = Line(left, right)

		self.play(Create(ruler))

		def x_to_point(x):
			alpha = x / L
			return ruler.point_from_proportion(alpha)


		tick_height = 0.2
		ticks = VGroup()
		labels = VGroup()
		for m in marks:
			p = x_to_point(m)
			tick = Line(p + UP * tick_height, p + DOWN * tick_height)
			ticks.add(tick)
			label = Text(str(m), font_size=28).next_to(p, DOWN, buff=0.3)
			labels.add(label)

		self.play(Create(ticks), Write(labels))
		self.wait(0.5)


		for d in range(1, L+1):
			# Chercher une paire (a,b) telle que b - a = d
			pair = None
			for i in range(len(marks)):
				for j in range(i + 1, len(marks)):
					if marks[j] - marks[i] == d:
						pair = (marks[i], marks[j])
						break
				if pair:
					break

			if pair is None:
				continue

			a, b = pair
			pa = x_to_point(a)
			pb = x_to_point(b)

			segment = Line(pa, pb, color=YELLOW, stroke_width=6)
			d_label = MathTex(str(d), font_size=34).next_to(segment, UP, buff=0.25)

			self.play(Create(segment), FadeIn(d_label))
			self.wait(0.5)

			self.play(FadeOut(segment), FadeOut(d_label))

		self.wait(1)