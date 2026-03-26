"""
Animation 3 : Couverture complète des distances
Remplissage dynamique de la grille des différences modulaires.
"""

from manim import *
import numpy as np

class DobbleAllDistances(Scene):
    def construct(self):
        self.camera.background_color = "#000104"
        
        # --- PARAMÈTRES ---
        N = 7
        RULE = [0, 1, 3] # La règle parfaite
        RADIUS = 2.0
        CIRCLE_CENTER = 3.5 * LEFT
        GRID_CENTER = 2.5 * RIGHT
        
        # --- TITRE ---
        title = Text("Propriété de la Règle Parfaite", font_size=36, color=GOLD).to_edge(UP)
        subtitle = Text("Chaque distance 1..6 apparaît exactement une fois", font_size=24, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        
        # --- SETUP CERCLE (GAUCHE) ---
        circle = Circle(radius=RADIUS, color=BLUE_E, stroke_width=4).move_to(CIRCLE_CENTER)
        self.play(Create(circle))
        
        # Placer les points de la règle
        dots = VGroup()
        dot_pos_map = {} # map value -> position
        
        for val in RULE:
            angle = TAU * val / N
            pos = CIRCLE_CENTER + RADIUS * np.array([np.cos(angle), np.sin(angle), 0])
            
            d = Dot(pos, color=YELLOW, radius=0.15)
            lbl = Text(str(val), font_size=20, weight=BOLD).next_to(pos, direction=pos-CIRCLE_CENTER, buff=0.2)
            
            dots.add(d, lbl)
            dot_pos_map[val] = pos
            
        self.play(FadeIn(dots))
        
        # --- SETUP GRILLE (DROITE) ---
        # On veut montrer que les distances {1, 2, 3, 4, 5, 6} sont toutes atteintes.
        # On fait une grille 1x6 horizontale ou verticale ?
        # Verticale est mieux pour lister les calculs à côté.
        
        grid_group = VGroup()
        cells = {} # map distance -> square object
        
        # Création des cases vides 1..6
        for dist in range(1, N):
            # Case
            square = Square(side_length=0.8, color=WHITE, stroke_opacity=0.5)
            # Position : Grille 2x3 pour faire joli ? ou 1x6 ?
            # Faisons 1 colonne verticale
            pos = GRID_CENTER + (3.5 - dist) * 0.9 * UP # Empilés
            square.move_to(pos)
            
            # Label numéro
            num = Text(str(dist), font_size=24, color=GRAY).move_to(pos)
            
            # Label calcul (vide au début) à droite de la case
            calc_lbl = Text("", font_size=20, color=YELLOW).next_to(square, RIGHT, buff=0.4)
            
            grid_group.add(square, num, calc_lbl)
            cells[dist] = {"sq": square, "num": num, "calc": calc_lbl, "filled": False}
            
        self.play(FadeIn(grid_group))
        
        # --- CALCUL DYNAMIQUE ---
        # On itère sur toutes les paires ordonnées de la règle
        # Pour couvrir 1..6, il faut prendre (b-a) mod 7 pour tout a!=b
        
        pairs_to_check = []
        for i in range(len(RULE)):
            for j in range(len(RULE)):
                if i != j:
                    pairs_to_check.append((RULE[i], RULE[j]))
        
        # Animation boucle
        for p1, p2 in pairs_to_check:
            # 1. Calcul distance
            dist = (p2 - p1) % N
            
            # 2. Tracer flèche sur le cercle
            start_pos = dot_pos_map[p1]
            end_pos = dot_pos_map[p2]
            
            # Flèche courbe
            arrow = CurvedArrow(start_pos, end_pos, angle=-TAU/4, color=YELLOW)
            # Label calcul temporaire au centre cercle ?
            calc_txt = MathTex(f"{p2} - {p1} \\equiv {dist}", color=YELLOW, font_size=32).move_to(CIRCLE_CENTER)
            
            self.play(Create(arrow), Write(calc_txt), run_time=0.8)
            
            # 3. Remplir la case correspondante
            cell = cells[dist]
            
            if cell["filled"]:
                # Aie, collision ! (Ne devrait pas arriver avec une règle parfaite)
                self.play(cell["sq"].animate.set_color(RED))
            else:
                # Succès
                # Animer le carré -> Vert plein
                self.play(
                    cell["sq"].animate.set_fill(GREEN, opacity=0.8).set_stroke(GREEN),
                    cell["num"].animate.set_color(WHITE).scale(1.2),
                    run_time=0.5
                )
                
                # Afficher le calcul à côté
                final_calc = Text(f"{p2}-{p1}", font_size=20, color=GREEN_A).move_to(cell["calc"].get_center())
                self.play(Transform(cell["calc"], final_calc))
                
                cell["filled"] = True
            
            self.wait(0.5)
            self.play(FadeOut(arrow), FadeOut(calc_txt), run_time=0.3)
            
        # --- CONCLUSION ---
        # Vérifier si tout est rempli
        all_filled = all(c["filled"] for c in cells.values())
        
        if all_filled:
            final_txt = Text("Grille Complète : C'est une Règle Parfaite !", font_size=28, color=GOLD).to_edge(DOWN)
            self.play(Write(final_txt))
            # Petit effet de célébration sur la grille
            self.play(grid_group.animate.scale(1.1), run_time=0.5)
            self.play(grid_group.animate.scale(1/1.1), run_time=0.5)
            
        self.wait(3)

# config.quality = "high_quality"
