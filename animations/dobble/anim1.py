from manim import *
import numpy as np

class DobbleCompareFluid(Scene):
    def construct(self):
        
        N = 7
        RULE = [1, 2, 4] 
        REF_SYMBOLS = RULE
        
        RADIUS = 1.8
        LEFT_CENTER = 3.5 * LEFT
        RIGHT_CENTER = 3.5 * RIGHT
        
        
        title = Text("Propriété Fondamentale Dobble", font_size=36, color=GOLD).to_edge(UP)
        self.play(Write(title))
        

        c_left = Circle(radius=RADIUS, color=BLUE_E, stroke_width=4).move_to(LEFT_CENTER)
        c_right = Circle(radius=RADIUS, color=BLUE_E, stroke_width=4).move_to(RIGHT_CENTER)
        
        self.play(Create(c_left), Create(c_right), run_time=1.5)
        
        
        def get_ticks(center):
            ticks = VGroup()
            for i in range(N):
                angle = TAU * i / N
                pos = center + RADIUS * np.array([np.cos(angle), np.sin(angle), 0])
                tick = Line(center, pos).scale(0.1).move_to(pos).set_color(WHITE)
                label = Text(str(i), font_size=20, color=WHITE).move_to(center + (RADIUS + 0.5) * np.array([np.cos(angle), np.sin(angle), 0]))
                ticks.add(tick, label)
            return ticks
        
        ticks_l = get_ticks(LEFT_CENTER)
        ticks_r = get_ticks(RIGHT_CENTER)
        self.play(FadeIn(ticks_l), FadeIn(ticks_r), run_time=1.5, rate_func=smooth)
        
        lbl_l = Text("Carte Référence {1,2,4}", font_size=20, color=BLUE).next_to(c_left, DOWN, buff=0.8)
        lbl_r = Text("Carte Rotative", font_size=20, color=BLUE).next_to(c_right, DOWN, buff=0.8)
        self.play(Write(lbl_l), Write(lbl_r))
        
        
        # GAUCHE (Fixe)
        left_dots = VGroup()
        for s in REF_SYMBOLS:
            angle = TAU * s / N
            pos = LEFT_CENTER + RADIUS * np.array([np.cos(angle), np.sin(angle), 0])
            dot = Dot(pos, color=YELLOW, radius=0.15)
            ring = Circle(radius=0.25, color=YELLOW).move_to(pos)
            left_dots.add(dot, ring)
        self.play(FadeIn(left_dots))
        
        # DROITE (Mobile)
        rotator = VGroup()
        for base_s in RULE:
            angle = TAU * base_s / N
            rel_pos = RADIUS * np.array([np.cos(angle), np.sin(angle), 0])
            dot = Dot(rel_pos, color=YELLOW, radius=0.15) 
            rotator.add(dot)
        
        
        rotator.move_to(RIGHT_CENTER) 
        
        rotator = VGroup()
        for base_s in RULE:
            angle = TAU * base_s / N
            pos = RIGHT_CENTER + RADIUS * np.array([np.cos(angle), np.sin(angle), 0])
            dot = Dot(pos, color=YELLOW, radius=0.15)
            dot.offset_index = base_s 
            rotator.add(dot)
            
        self.play(FadeIn(rotator))
        
        info_label = Text("", font_size=24).move_to(ORIGIN)
        
        current_shift = 0
        
        temp_lines = VGroup()
        
        for step in range(N):
            
            current_right_syms = [(x + current_shift) % N for x in RULE]
            
            common = []
            for s in current_right_syms:
                if s in REF_SYMBOLS:
                    common.append(s)
            
            new_lines = VGroup()
            highlights = VGroup()
            
            for dot in rotator:
                sym = (dot.offset_index + current_shift) % N
                
                if sym in common:
                    angle_l = TAU * sym / N
                    pos_l = LEFT_CENTER + RADIUS * np.array([np.cos(angle_l), np.sin(angle_l), 0])
                    line = Line(pos_l, dot.get_center(), color=GREEN, stroke_width=4)
                    new_lines.add(line)
                    
                    hl = Circle(radius=0.25, color=GREEN).move_to(dot.get_center())
                    highlights.add(hl)
                    
                    dot.set_color(GREEN)
                else:
                    dot.set_color(YELLOW)
            

            if len(common) == 3:
                txt = "Identiques !"
                col = RED
            else:
                txt = f"Commun : {common[0]}"
                col = GREEN
            
            new_label = Text(txt, font_size=24, color=col).move_to(ORIGIN)
            

            self.play(
                Create(new_lines), 
                FadeIn(highlights), 
                Transform(info_label, new_label),
                run_time=0.5
            )
            self.wait(0.8)
            

            self.play(
                FadeOut(new_lines), 
                FadeOut(highlights), 
                run_time=0.3
            )
            
            
            self.play(
                Rotate(
                    rotator, 
                    angle=TAU/N, 
                    about_point=RIGHT_CENTER, 
                    run_time=1.0,
                    rate_func=smooth
                )
            )
            
            current_shift = (current_shift + 1) % N
            
        
        self.wait(2)
