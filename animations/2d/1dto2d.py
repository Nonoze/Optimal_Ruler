"""
Animation 4 : Transition 1D vers 2D
Concept : Règle linéaire (scalaire) -> Grille 2D (vecteurs)
"""

from manim import *
import numpy as np

class Transition1Dto2D(Scene):
    def construct(self):
        # self.camera.background_color = "#000104"
        
        # --- PARTIE 1 : RÈGLE 1D ---
        
        ruler_1d = NumberLine(
            x_range=[0, 6, 1],
            length=6,
            color=BLUE,
            include_numbers=True,
            label_direction=DOWN
        )
        self.play(Create(ruler_1d))
        
        title = Text("Règle 1D : Distances Scalaires", font_size=32).to_edge(UP)
        self.play(Write(title))
        
        p1 = ruler_1d.n2p(1)
        p2 = ruler_1d.n2p(4)
        
        brace = BraceBetweenPoints(p1, p2, direction=UP)
        dist_lbl = brace.get_text("Distance = 3")
        
        dot1 = Dot(p1, color=YELLOW)
        dot2 = Dot(p2, color=YELLOW)
        
        self.play(FadeIn(dot1), FadeIn(dot2))
        self.play(GrowFromCenter(brace), Write(dist_lbl))
        self.wait(1)
        
        # Nettoyage partiel pour transition
        self.play(FadeOut(brace), FadeOut(dist_lbl), FadeOut(dot1), FadeOut(dot2))
        
        # --- PARTIE 2 : TRANSITION VERS 2D ---
        
        new_title = Text("Règle 2D : Distances Vectorielles", font_size=32).to_edge(UP)
        
        # On va transformer la NumberLine en Axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True},
            tips=False
        ).center()
        
        # Animation : L'axe X reste (à peu près), l'axe Y "pousse" vers le haut
        # On remplace ruler_1d par axes.x_axis visuellement d'abord
        # Puis on fait pousser y_axis
        
        self.play(Transform(title, new_title))
        
        # Déplacer ruler_1d pour qu'elle corresponde à axes.x_axis
        self.play(Transform(ruler_1d, axes.x_axis))
        
        # Faire pousser l'axe Y
        self.play(Create(axes.y_axis))
        
        # Faire apparaître la grille (points)
        # On crée une grille de points pour matérialiser l'espace 2D
        grid_dots = VGroup()
        for x in range(5):
            for y in range(5):
                d = Dot(axes.c2p(x+1, y+1), color=GRAY, radius=0.05)
                grid_dots.add(d)
        
        self.play(FadeIn(grid_dots, lag_ratio=0.05), run_time=2)
        
        # --- PARTIE 3 : VECTEURS ---
        
        # Exemple 1 : Vecteur horizontal (analogue à 1D)
        # (1,2) -> (4,2)
        v1_start = axes.c2p(1, 2)
        v1_end = axes.c2p(4, 2)
        
        arrow1 = Arrow(v1_start, v1_end, buff=0, color=YELLOW)
        lbl1 = MathTex(r"\vec{v} = (3, 0)", color=YELLOW).next_to(arrow1, DOWN)
        
        self.play(Create(arrow1), Write(lbl1))
        self.wait(1)
        
        # Exemple 2 : Vecteur vertical
        # (4,2) -> (4,4)
        v2_start = axes.c2p(4, 2)
        v2_end = axes.c2p(4, 4)
        
        arrow2 = Arrow(v2_start, v2_end, buff=0, color=GREEN)
        lbl2 = MathTex(r"\vec{u} = (0, 2)", color=GREEN).next_to(arrow2, RIGHT)
        
        self.play(Create(arrow2), Write(lbl2))
        self.wait(1)
        
        # Exemple 3 : Vecteur diagonal (La nouveauté !)
        # (1,2) -> (4,4)  (Somme des deux précédents)
        v3_start = axes.c2p(1, 2)
        v3_end = axes.c2p(4, 4)
        
        arrow3 = Arrow(v3_start, v3_end, buff=0, color=RED, stroke_width=4)
        lbl3 = MathTex(r"\vec{w} = (3, 2)", color=RED).next_to(arrow3.get_center(), UP+LEFT)
        
        # On peut montrer que c'est une "différence de positions"
        # P2 - P1 = (4-1, 4-2) = (3,2)
        
        self.play(Create(arrow3), Write(lbl3))
        self.wait(2)
        
        # Conclusion
        final_txt = Text("En 2D, on mesure des différences de vecteurs (Δx, Δy)", font_size=24, color=GOLD).to_edge(DOWN)
        self.play(Write(final_txt))
        self.wait(3)