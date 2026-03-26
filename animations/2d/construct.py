"""
Animation 5 : Construction Borne Sup 2L (Version Grille Discrète)
Grille 9x9 explicite.
"""

from manim import *
import numpy as np

class CurSolution2D(Scene):
    def construct(self):
        self.camera.background_color = "#000104"
        
        # --- PARAMÈTRES ---
        L = 9
        SQRT_L = 3
        SPACING = 0.6  # Espacement entre points
        
        # --- TITRES (plus haut pour éviter collision) ---
        title = Text(f"Borne Supérieure: 2L (Cas L=9)", font_size=32, color=GOLD).to_edge(UP, buff=0.2)
        
        # --- CRÉATION DE LA GRILLE DE FOND ---
        # On crée 81 petits points gris pour matérialiser l'espace L x L
        grid_dots = VGroup()
        grid_coords = {} # (x,y) -> Dot object
        
        # Centrage : grille 9x9 -> de -4 à +4 unités relatives
        center_offset = (L-1) * SPACING / 2
        
        for x in range(L):
            for y in range(L):
                # Position centrée
                pos = np.array([x * SPACING - center_offset, y * SPACING - center_offset - 0.5, 0])
                
                # Point gris discret
                d = Dot(pos, color=GRAY_E, radius=0.06)
                grid_dots.add(d)
                grid_coords[(x,y)] = d
                
        self.play(Write(title))
        self.play(FadeIn(grid_dots), run_time=1.5)
        
        # --- PHASE DIVISION (Lignes de séparation) ---
        # On veut séparer visuellement les blocs 3x3
        
        separators = VGroup()
        # Lignes verticales
        for i in range(1, int(L/SQRT_L)):
            # x index = i * 3
            # position x = (i*3 - 0.5) * SPACING - center_offset ? 
            # Non, entre les colonnes 2 et 3 (indices).
            # Entre index (i*3-1) et (i*3).
            
            x_pos = (i * SQRT_L * SPACING) - center_offset - (SPACING/2)
            line = Line(
                start=[x_pos, -center_offset - 0.5 - SPACING, 0],
                end=[x_pos, center_offset - 0.5 + SPACING, 0],
                color=BLUE, stroke_opacity=0.7, stroke_width=2
            )
            separators.add(line)
            
        # Lignes horizontales
        for j in range(1, int(L/SQRT_L)):
            y_pos = (j * SQRT_L * SPACING) - center_offset - 0.5 - (SPACING/2)
            line = Line(
                start=[-center_offset - SPACING, y_pos, 0],
                end=[center_offset + SPACING, y_pos, 0],
                color=BLUE, stroke_opacity=0.7, stroke_width=2
            )
            separators.add(line)
            
        self.play(Create(separators))
        
        # --- PHASE DENSE (Bloc Bas-Gauche 3x3) ---
        dense_group = VGroup()
        for x in range(SQRT_L):
            for y in range(SQRT_L):
                dot = grid_coords[(x,y)]
                # On transforme le point gris en point JAUNE brillant
                dense_group.add(dot)
        
        self.play(
            dense_group.animate.set_color(YELLOW).set_radius(0.12),
            run_time=1.5
        )
        
        lbl_dense = Text("1. Bloc Dense (complet)", font_size=20, color=YELLOW).next_to(grid_dots, LEFT, buff=0.7)
        self.play(Write(lbl_dense))
        
        # --- PHASE SPARSE (1 point par autre bloc) ---
        # On met le point au coin bas-gauche local de chaque bloc 3x3
        sparse_group = VGroup()
        
        for bx in range(int(L/SQRT_L)):
            for by in range(int(L/SQRT_L)):
                if bx == 0 and by == 0: continue # Skip dense block
                
                # Coordonnées globales du coin supérieur droit du bloc
                gx = bx * SQRT_L + SQRT_L - 1
                gy = by * SQRT_L + SQRT_L - 1
                
                dot = grid_coords[(gx, gy)]
                sparse_group.add(dot)
                
        self.play(
            sparse_group.animate.set_color(GREEN).set_radius(0.12),
            run_time=1.5
        )
        
        lbl_sparse = Text("2. Points Pivots\n(1 par bloc)", font_size=20, color=GREEN).next_to(grid_dots, RIGHT, buff=0.7)
        self.play(Write(lbl_sparse))
        
        # --- EXEMPLE VECTEUR ---
        # On efface les textes latéraux pour clarté
        self.play(FadeOut(lbl_dense), FadeOut(lbl_sparse))
        
        p_start = grid_coords[(1, 1)].get_center() # Dans zone dense
        p_end = grid_coords[(8, 5)].get_center()   # Dans zone sparse (bloc 2,1)
        
        vec = Arrow(p_start, p_end, buff=0, color=RED)
        lbl_vec = MathTex(r"\vec{v}", color=RED).next_to(vec, UP)
        
        self.play(Create(vec), Write(lbl_vec))

        # Décaler tous les éléments vers la gauche pour faire de la place à l'explication finale
        all_elements = VGroup(grid_dots, separators, dense_group, sparse_group, vec, lbl_vec)
        self.play(all_elements.animate.shift(3*LEFT), run_time=1.5)
        
        # Texte explicatif final à droite
        txt_explicatif = Text("Tous les vecteurs peuvent être tracés\nen prenant un point jaune comme\ndépart et le point vert du sous-carré\ncorrespondant comme arrivée.", font_size=24, color=GOLD).to_edge(RIGHT)
        self.play(Write(txt_explicatif))
        self.wait(4)

        self.play(FadeOut(vec), FadeOut(lbl_vec), FadeOut(txt_explicatif), all_elements.animate.shift(3*RIGHT), run_time=1.5)
        self.wait(0.5)

        # montrer tous les vecteurs possibles ansi que les points de départ/arrivée

        for compo_x in [3, 4, 5]:
            for compo_y in [3, 4, 5]:
                
                temp_vec = Arrow(grid_coords[(0, 0)].get_center(), grid_coords[(compo_x, compo_y)].get_center(), buff=0, color=RED, stroke_width=2, stroke_opacity=0.3)
                self.play(Create(temp_vec), run_time=0.5)

                start_x = SQRT_L - (compo_x % SQRT_L) - 1
                start_y = SQRT_L - (compo_y % SQRT_L) - 1
                start_vec = grid_coords[start_x, start_y].get_center()
                end_vec = grid_coords[(compo_x + start_x, compo_y + start_y)].get_center()
                real_vec = Arrow(start_vec, end_vec, buff=0, color=YELLOW, stroke_width=3, tip_length=0.15)

                # On diminue la taille du triangle du bout de la flèche


                self.play(Transform(temp_vec, real_vec), run_time=0.5)
                self.wait(0.4)
                self.play(FadeOut(real_vec), run_time=0.3)
        self.wait(3)

# config.quality = "high_quality"
