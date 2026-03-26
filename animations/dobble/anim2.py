"""
Animation 2 ALTERNATIVE : Force Brute entre 2 Cartes
Trace toutes les lignes possibles entre Carte A et Carte B pour trouver les coïncidences.
"""

from manim import *
import numpy as np

class DobbleBruteForce(Scene):
    def construct(self):
        self.camera.background_color = "#000104"
        
        N = 7
        RULE = [0, 1, 3]
        SHIFT = 2 # Comparons Carte 0 {0,1,3} et Carte 2 {2,3,5} (Intersection attendue: 3)
        
        RADIUS = 1.8
        LEFT_CENTER = 3.5*LEFT
        RIGHT_CENTER = 3.5*RIGHT
        
        # Setup
        c1 = Circle(radius=RADIUS).move_to(LEFT_CENTER)
        c2 = Circle(radius=RADIUS).move_to(RIGHT_CENTER)
        self.play(Create(c1), Create(c2))
        
        # Points C1 {0,1,3}
        p1_coords = []
        for p in RULE:
            angle = TAU*p/N
            pos = LEFT_CENTER + RADIUS*np.array([np.cos(angle), np.sin(angle), 0])
            d = Dot(pos, color=YELLOW)
            lbl = Text(str(p), font_size=16).next_to(pos, OUT) # OUT éloigne du centre ? non, juste shift
            lbl.move_to(LEFT_CENTER + (RADIUS+0.3)*np.array([np.cos(angle), np.sin(angle), 0]))
            self.add(d, lbl)
            p1_coords.append((p, pos))
            
        # Points C2 {2,3,5}
        p2_coords = []
        targets = [(x+SHIFT)%N for x in RULE]
        for p in targets:
            angle = TAU*p/N
            pos = RIGHT_CENTER + RADIUS*np.array([np.cos(angle), np.sin(angle), 0])
            d = Dot(pos, color=YELLOW)
            lbl = Text(str(p), font_size=16)
            lbl.move_to(RIGHT_CENTER + (RADIUS+0.3)*np.array([np.cos(angle), np.sin(angle), 0]))
            self.add(d, lbl)
            p2_coords.append((p, pos))
            
        # TRACER TOUTES LES LIGNES ET COMPARER
        # On compare les VALEURS des symboles
        
        matches = 0
        
        for val1, pos1 in p1_coords:
            for val2, pos2 in p2_coords:
                # Ligne de test
                line = Line(pos1, pos2, color=GRAY, stroke_opacity=0.3)
                self.play(Create(line), run_time=0.2)
                
                # Check
                if val1 == val2:
                    line.set_color(GREEN).set_opacity(1).set_stroke(width=4)
                    matches += 1
                    # Pulse
                    self.play(Indicate(line, color=GREEN))
                else:
                    self.play(FadeOut(line), run_time=0.1)
                    
        txt = Text(f"Total Intersections : {matches}", font_size=32, color=GREEN).to_edge(UP)
        self.play(Write(txt))
        self.wait(2)