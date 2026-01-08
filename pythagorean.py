from manim import *
import numpy as np

class righttriangle(Scene):
    def construct(self):
        # Zoom out to fit everything on screen
        self.camera.frame_width = 20
        self.camera.frame_height = 12
        
        # Triangle vertices: A (top), B (left), C (right)
        # (These points also define the label coordinates below.)
        pA = np.array([-0.7, 2.0, 0])  # A
        pB = np.array([-2.5, -0.4, 0])  # B
        pC = np.array([2.5, -0.4, 0])  # C

        # Create the triangle using the Polygon mobject
        triangle = Polygon(pA, pB, pC, color=WHITE, stroke_width=2)
        
        # Create the lines forming the right angle
        line1 = Line(pB, pA)
        line2 = Line(pC, pA)
        
        # Create the right angle indicator
        right_angle = RightAngle(line1, line2, length=0.4, quadrant=(-1,-1))
        
        # Labels (hard-coded coordinates; no label-position calculations)
        label_A = MathTex("A").move_to([-0.85, 2.30, 0])
        label_B = MathTex("B").move_to([-2.75, -0.65, 0])
        label_C = MathTex("C").move_to([2.75, -0.65, 0])
        
        # Step 1: Create triangle
        self.play(Create(triangle))
        self.play(Write(label_A), Write(label_B), Write(label_C))
        self.wait(0.5)
        self.play(Create(right_angle))
        self.wait(0.5)
        
        # Step 2: Create squares
        square1 = self.square_on_side(pB, pC, pA, 5.0, BLUE)
        square2 = self.square_on_side(pA, pC, pB, 4, PINK)
        square3 = self.square_on_side(pA, pB, pC, 3, GREEN)
        self.play(Create(square1), Create(square2), Create(square3), run_time=1.5)
        
        # Square vertex labels
        label_D = MathTex("D").move_to([-2.7475, -5.6475, 0])
        label_E = MathTex("E").move_to([2.7475, -5.6475, 0])
        label_F = MathTex("F").move_to([-3.1495, 4.1465, 0])
        label_G = MathTex("G").move_to([-5.2465, 1.3505, 0])
        label_H = MathTex("H").move_to([5.2465, 2.8495, 0])
        label_K = MathTex("K").move_to([1.6505, 5.5465, 0])
        self.play(Write(VGroup(label_D, label_E, label_F, label_G, label_H, label_K)))
        self.wait(0.5)
        
        # Step 3: Create dotted lines
        # Height from A to BC: M is the foot, and AM is dotted
        pM = np.array([-0.7, -0.4, 0])   # on BC
        dot_M = Dot(pM, color=WHITE, radius=0.05)
        label_M = MathTex("M").move_to([-1.0, -0.1, 0])
        dashed_AM = DashedLine(pA, pM, color=WHITE, stroke_width=2, dash_length=0.08)
        
        # Extend AM down to DE; intersection point is L
        pD = np.array([-2.5, -5.4, 0])
        pE = np.array([2.5, -5.4, 0])
        pL = np.array([-0.7, -5.4, 0])
        dot_L = Dot(pL, color=WHITE, radius=0.05)
        label_L = MathTex("L").move_to([-1.0, -5.8, 0])
        dashed_ML = DashedLine(pM, pL, color=WHITE, stroke_width=2, dash_length=0.08)
        
        # Extra dotted lines: AD and GC
        # F is chosen so that F-A-C are collinear (FAC is a straight line)
        pF = np.array([-3.1, 3.8, 0])
        pG = np.array([-4.9, 1.4, 0])
        dashed_AD = DashedLine(pA, pD, color=WHITE, stroke_width=2, dash_length=0.08)
        dashed_GC = DashedLine(pG, pC, color=WHITE, stroke_width=2, dash_length=0.08)
        
        self.play(Create(dashed_AM), FadeIn(dot_M), Write(label_M))
        self.play(Create(dashed_ML), FadeIn(dot_L), Write(label_L))
        self.play(Create(dashed_AD), Create(dashed_GC))
        self.wait(2)

        # 1) Right angle indicator on FAB (same size as the other one)
        line_AF = Line(pA, pF)
        line_AB = Line(pA, pB)
        right_angle_FAB = RightAngle(line_AB, line_AF, length=0.4, quadrant=(1, -1), color=YELLOW)
        right_angle_FAB.set_z_index(50)
        self.play(Create(right_angle_FAB))

        # 2) Highlight the line FAC + explanation text
        highlight_FAC = Line(pF, pC, color=YELLOW, stroke_width=8)
        explain_FAC = Text(
            "FAC is a staight line,\nFA and AC lie on the same line",
            font_size=28,
        ).move_to([7.2, 1.6, 0])
        self.play(Create(highlight_FAC), Write(explain_FAC))
        self.wait(2)

        # 3) Fade out steps 1 and 2
        self.play(FadeOut(right_angle_FAB), FadeOut(highlight_FAC), FadeOut(explain_FAC))

        # 4) Make everything unfilled and white
        self.play(
            square1.animate.set_fill(opacity=0).set_stroke(WHITE, width=2),
            square2.animate.set_fill(opacity=0).set_stroke(WHITE, width=2),
            square3.animate.set_fill(opacity=0).set_stroke(WHITE, width=2),
        )

        # 5) Highlight triangle GBC (orange, slightly filled)
        tri_GBC = Polygon(pG, pB, pC).set_stroke(ORANGE, width=3).set_fill(ORANGE, opacity=0.25)
        self.play(FadeIn(tri_GBC))

        # Make smaller duplicate of triangle GBC (before highlighting ABD)
        # - mini_GBC: left of main shape, above the "GB = AB ..." text area
        mini_scale = 0.75
        # mini_GBC: shrink, then move
        mini_GBC = tri_GBC.copy().scale(mini_scale)
        self.play(TransformFromCopy(tri_GBC, mini_GBC), run_time=1.0)
        self.wait(0.6)
        self.play(mini_GBC.animate.move_to([-6.3, -1.2, 0]), run_time=1.0)
        self.wait(0.8)

        # Small labels for mini GBC (after it has moved)
        g2, b2, c2 = mini_GBC.get_vertices()  # G', B', C'
        center_gbc = mini_GBC.get_center()
        mini_G_label = MathTex("G").scale(0.6).move_to(g2 + (g2 - center_gbc) / np.linalg.norm(g2 - center_gbc) * 0.25)
        mini_B_label_1 = MathTex("B").scale(0.6).move_to(b2 + (b2 - center_gbc) / np.linalg.norm(b2 - center_gbc) * 0.25)
        mini_C_label = MathTex("C").scale(0.6).move_to(c2 + (c2 - center_gbc) / np.linalg.norm(c2 - center_gbc) * 0.25)
        self.play(Write(VGroup(mini_G_label, mini_B_label_1, mini_C_label)))
        self.wait(0.6)

        # 6) Highlight triangle ABD (purple, slightly filled)
        tri_ABD = Polygon(pA, pB, pD).set_stroke(PURPLE, width=3).set_fill(PURPLE, opacity=0.25)
        self.play(FadeIn(tri_ABD))
        self.wait(1.2)

        # Make smaller duplicate of triangle ABD
        # - mini_ABD: below mini_GBC, rotated so mini_BC || mini_BD
        mini_ABD = tri_ABD.copy().scale(mini_scale)
        self.play(TransformFromCopy(tri_ABD, mini_ABD), run_time=1.0)
        self.wait(0.6)
        self.play(mini_ABD.animate.rotate(PI / 2).move_to([-6.3, -2.8, 0]), run_time=1.2)
        self.wait(0.8)

        # Small labels for mini ABD (after it has rotated+moved)
        a2, b3, d2 = mini_ABD.get_vertices()  # A', B', D'
        center_abd = mini_ABD.get_center()
        mini_A_label = MathTex("A").scale(0.6).move_to(a2 + (a2 - center_abd) / np.linalg.norm(a2 - center_abd) * 0.25)
        mini_B_label_2 = MathTex("B").scale(0.6).move_to(b3 + (b3 - center_abd) / np.linalg.norm(b3 - center_abd) * 0.25)
        mini_D_label = MathTex("D").scale(0.6).move_to(d2 + (d2 - center_abd) / np.linalg.norm(d2 - center_abd) * 0.25)
        self.play(Write(VGroup(mini_A_label, mini_B_label_2, mini_D_label)))
        self.wait(0.6)

        # Cache mini triangle vertices for notch/line steps later (order preserved from Polygon)
        # (g2, b2, c2 already cached above)
        # (a2, b3, d2 already cached above)

        # 7) Single notch on GB and AB + thicker red lines
        line_GB_red = Line(pG, pB).set_stroke(RED, width=6)
        line_AB_red = Line(pA, pB).set_stroke(RED, width=6)
        notch_GB = self.tick_marks(pG, pB, n=1, color=RED)
        notch_AB = self.tick_marks(pA, pB, n=1, color=RED)
        # Apply the same to the mini triangles: (G'B') and (A'B')
        line_GB_red_mini = Line(g2, b2).set_stroke(RED, width=6)
        line_AB_red_mini = Line(a2, b3).set_stroke(RED, width=6)
        notch_GB_mini = self.tick_marks(g2, b2, n=1, color=RED)
        notch_AB_mini = self.tick_marks(a2, b3, n=1, color=RED)
        self.play(
            Create(line_GB_red), Create(line_AB_red), FadeIn(notch_GB), FadeIn(notch_AB),
            Create(line_GB_red_mini), Create(line_AB_red_mini), FadeIn(notch_GB_mini), FadeIn(notch_AB_mini),
        )
        self.wait(0.9)

        # 8) Write "GB=AB" bottom-left
        text_GB_AB = Text("GB = AB (same sides on a square)", font_size=28).move_to([-5.8, -4.8, 0])
        self.play(Write(text_GB_AB))
        self.wait(1.2)

        # 9) Double notch on BC and BD + thicker blue lines
        line_BC_blue = Line(pB, pC).set_stroke(BLUE, width=6)
        line_BD_blue = Line(pB, pD).set_stroke(BLUE, width=6)
        notch_BC = self.tick_marks(pB, pC, n=2, color=BLUE)
        notch_BD = self.tick_marks(pB, pD, n=2, color=BLUE)
        # Apply the same to the mini triangles: (B'C') and (B'D')
        line_BC_blue_mini = Line(b2, c2).set_stroke(BLUE, width=6)
        line_BD_blue_mini = Line(b3, d2).set_stroke(BLUE, width=6)
        notch_BC_mini = self.tick_marks(b2, c2, n=2, color=BLUE)
        notch_BD_mini = self.tick_marks(b3, d2, n=2, color=BLUE)
        self.play(
            Create(line_BC_blue), Create(line_BD_blue), FadeIn(notch_BC), FadeIn(notch_BD),
            Create(line_BC_blue_mini), Create(line_BD_blue_mini), FadeIn(notch_BC_mini), FadeIn(notch_BD_mini),
        )
        self.wait(0.9)

        # 10) Write "BC=BD" bottom-left
        text_BC_BD = Text("BC = BD (same sides on a square)", font_size=28).move_to([-5.8, -5.6, 0])
        self.play(Write(text_BC_BD))
        self.wait(2)

        # --- After all that animation (angle relations) ---
        # 1) Remove the two equality texts
        self.play(FadeOut(text_GB_AB), FadeOut(text_BC_BD))
        self.wait(0.6)

        # 2) Highlight angle ABC (inside triangle ABC, at B)
        angle_ABC = Angle(Line(pB, pC), Line(pB, pA), radius=0.45, color=ORANGE, quadrant=(1, 1))
        self.play(Create(angle_ABC))
        self.wait(0.4)

        # 3) Highlight right angle GBA (at B)
        right_GBA = RightAngle(Line(pB, pG), Line(pB, pA), length=0.4, color=GREEN)
        self.play(Create(right_GBA))
        self.wait(0.4)

        # 4) Highlight angle GBC on the mini GBC (INTERIOR obtuse angle, at B)
        angle_mini_GBC = Angle(Line(b2, c2), Line(b2, g2), radius=0.30, color=GREEN, quadrant=(1, 1))
        self.play(Create(angle_mini_GBC))
        self.wait(0.4)

        # 5) Text under the mini triangles
        eq1 = MathTex(r"\angle GBC = \angle GBA + \angle ABC = 90^\circ + \angle ABC").scale(0.7)
        eq1.move_to([-6.0, -4, 0])
        self.play(Write(eq1))
        self.wait(0.6)

        # 6) Unhighlight angle GBA
        self.play(FadeOut(right_GBA))
        self.wait(0.4)

        # 7) Highlight right angle CBD (at B)
        right_CBD = RightAngle(Line(pB, pC), Line(pB, pD), length=0.4, color=BLUE)
        self.play(Create(right_CBD))
        self.wait(0.4)

        # 8) Highlight angle ABD on the mini ABD (INTERIOR obtuse angle, at B)
        angle_mini_ABD = Angle(Line(b3, d2), Line(b3, a2), radius=0.30, color=YELLOW, quadrant=(1, 1))
        self.play(Create(angle_mini_ABD))
        self.wait(0.4)

        # 9) Second text under the first
        eq2 = MathTex(r"\angle ABD = \angle CBD + \angle ABC = 90^\circ + \angle ABC").scale(0.7)
        eq2.move_to([-6.0, -4.6, 0])
        self.play(Write(eq2))
        self.wait(0.6)

        # 10) Conclusion under both
        eq3 = MathTex(r"\angle GBC = \angle ABD").scale(0.9)
        eq3.move_to([-6.0, -5.2, 0])
        self.play(Write(eq3))
        self.wait(0.6)

        # 11) Turn both highlighted (mini) angles the same color
        self.play(
            angle_mini_GBC.animate.set_color(GREEN).set_fill(GREEN, opacity=1),
            angle_mini_ABD.animate.set_color(GREEN).set_fill(GREEN, opacity=1),
        )
        self.wait(1.2)

        # Replace the equations with the SAS congruence statement
        self.play(FadeOut(eq1), FadeOut(eq2), FadeOut(eq3))
        sas = MathTex(r"\text{By SAS, }\triangle FBC \equiv \triangle ABD").scale(0.9)
        sas.move_to([-6.0, -4.7, 0])
        self.play(Write(sas))
        self.wait(2)

    def tick_marks(self, p1, p2, n=1, color=WHITE, size=0.25, spacing=0.35, stroke_width=4):
        """Draw 1 or 2 small tick marks (notches) across segment p1-p2."""
        p1 = np.array(p1, dtype=float)
        p2 = np.array(p2, dtype=float)
        v = p2 - p1
        v = v / np.linalg.norm(v)
        nvec = np.array([-v[1], v[0], 0.0])
        mid = (p1 + p2) / 2

        if n == 1:
            offsets = [0.0]
        else:
            offsets = [-spacing / 2, spacing / 2]

        marks = VGroup()
        for o in offsets[:n]:
            c = mid + v * o
            a = c - nvec * size / 2
            b = c + nvec * size / 2
            marks.add(Line(a, b).set_stroke(color, width=stroke_width))
        return marks
    
    def square_on_side(self, a, b, c, length, color):
        """Create a square on side ab, positioned outside the triangle"""
        square = Square(side_length=length, color=color, stroke_width=2, fill_opacity=0.5)
        mid = (np.array(a) + np.array(b)) / 2
        direction = np.array(b) - np.array(a)
        direction = direction / np.linalg.norm(direction)
        perp = np.array([-direction[1], direction[0], 0])
        if np.dot(np.array(c) - mid, perp) > 0:
            perp = -perp
        square.move_to(mid + perp * length/2)
        angle = np.arctan2(b[1]-a[1], b[0]-a[0])
        square.rotate(angle, about_point=square.get_center())
        return square

