from manim import *
import numpy as np


class PythagoreanTheorem(Scene):
    def construct(self):
        # Set up the right triangle ΔABC
        # Right angle at A, with A at top, B lower-left, C lower-right
        A = np.array([0, 1.5, 0])      # A at top
        B = np.array([-1.5, -1, 0])    # B lower-left
        C = np.array([1.5, -1, 0])     # C lower-right
        
        # Create the triangle
        triangle = Polygon(A, B, C, color=WHITE, stroke_width=3)
        
        # Label vertices
        label_A = MathTex("A", color=WHITE).scale(0.7).next_to(A, DOWN+LEFT, buff=0.15)
        label_B = MathTex("B", color=WHITE).scale(0.7).next_to(B, DOWN+RIGHT, buff=0.15)
        label_C = MathTex("C", color=WHITE).scale(0.7).next_to(C, UP+LEFT, buff=0.15)
        
        # Right angle marker
        right_angle = RightAngle(Line(A, B), Line(A, C), length=0.3, color=YELLOW)
        
        # Show triangle
        self.play(Create(triangle))
        self.play(
            Write(label_A),
            Write(label_B),
            Write(label_C),
            Create(right_angle)
        )
        self.wait(1)
        
        # Calculate side lengths
        AB_length = np.linalg.norm(B - A)  # 3
        AC_length = np.linalg.norm(C - A)  # 3
        BC_length = np.linalg.norm(C - B)  # sqrt(18) ≈ 4.24
        
        # Construct square ABFG on side AB
        # Square extends upward/left from AB
        AB_vec = B - A
        AB_perp = np.array([-AB_vec[1], AB_vec[0], 0])  # Perpendicular vector
        AB_perp_normalized = AB_perp / np.linalg.norm(AB_perp)
        # Choose direction that extends upward/left
        if AB_perp_normalized[1] < 0:  # If pointing down, flip
            AB_perp_normalized = -AB_perp_normalized
        F = B + AB_perp_normalized * AB_length
        G = A + AB_perp_normalized * AB_length
        square_ABFG = Polygon(A, B, F, G, color=BLUE, fill_opacity=0.3, stroke_width=2)
        
        # Label square vertices
        label_F = MathTex("F", color=BLUE).scale(0.6).next_to(F, UP+LEFT, buff=0.1)
        label_G = MathTex("G", color=BLUE).scale(0.6).next_to(G, UP+LEFT, buff=0.1)
        
        # Construct square ACKH on side AC
        # Square extends upward/right from AC
        AC_vec = C - A
        AC_perp = np.array([AC_vec[1], -AC_vec[0], 0])  # Perpendicular vector
        AC_perp_normalized = AC_perp / np.linalg.norm(AC_perp)
        # Choose direction that extends upward/right
        if AC_perp_normalized[1] < 0:  # If pointing down, flip
            AC_perp_normalized = -AC_perp_normalized
        K = C + AC_perp_normalized * AC_length
        H = A + AC_perp_normalized * AC_length
        square_ACKH = Polygon(A, C, K, H, color=GREEN, fill_opacity=0.3, stroke_width=2)
        
        # Label square vertices
        label_K = MathTex("K", color=GREEN).scale(0.6).next_to(K, UP+RIGHT, buff=0.1)
        label_H = MathTex("H", color=GREEN).scale(0.6).next_to(H, UP+RIGHT, buff=0.1)
        
        # Construct square BCED on hypotenuse BC
        # Square extends downward from BC
        BC_vec = C - B
        BC_normalized = BC_vec / BC_length
        BC_perp = np.array([-BC_normalized[1], BC_normalized[0], 0]) * BC_length
        # Choose direction that extends downward (below BC)
        if BC_perp[1] > 0:  # If pointing up, flip
            BC_perp = -BC_perp
        D = B + BC_perp
        E = C + BC_perp
        square_BCED = Polygon(B, C, E, D, color=RED, fill_opacity=0.3, stroke_width=2)
        
        # Label square vertices
        label_D = MathTex("D", color=RED).scale(0.6).next_to(D, DOWN, buff=0.1)
        label_E = MathTex("E", color=RED).scale(0.6).next_to(E, DOWN, buff=0.1)
        
        # Create squares (the "windmill")
        self.play(
            Create(square_ABFG),
            Create(square_ACKH),
            run_time=1.5
        )
        self.play(
            Write(label_F),
            Write(label_G),
            Write(label_K),
            Write(label_H)
        )
        self.wait(0.5)
        
        self.play(Create(square_BCED), run_time=1.5)
        self.play(
            Write(label_D),
            Write(label_E)
        )
        self.wait(1)
        
        # Draw line AL through A perpendicular to BC
        # AL is perpendicular to BC and extends through square BCED
        # M is the foot of the perpendicular from A to BC (where AL intersects BC)
        # L is where AL intersects DE (the bottom side of square BCED)
        
        # Find M: foot of perpendicular from A to BC
        BC_vec = C - B
        BC_length_sq = np.dot(BC_vec, BC_vec)
        t = np.dot(A - B, BC_vec) / BC_length_sq if BC_length_sq > 0.001 else 0
        M = B + t * BC_vec  # Point M on BC
        
        # Direction perpendicular to BC (pointing downward toward square)
        BC_normalized = BC_vec / np.linalg.norm(BC_vec) if np.linalg.norm(BC_vec) > 0.001 else np.array([1, 0, 0])
        perp_to_BC = np.array([-BC_normalized[1], BC_normalized[0], 0])
        # Make sure it points downward (toward D and E)
        if perp_to_BC[1] > 0:
            perp_to_BC = -perp_to_BC
        
        # Find L: intersection of AL with DE (bottom side of square BCED)
        # Line AL: A + s * perp_to_BC (perpendicular to BC)
        # Line DE: D + u * (E - D)
        DE_vec = E - D
        
        # Find intersection: A + s*perp_to_BC = D + u*DE_vec
        # Rearranged: s*perp_to_BC - u*DE_vec = D - A
        M_intersect = np.array([[perp_to_BC[0], -DE_vec[0]],
                                 [perp_to_BC[1], -DE_vec[1]]])
        b_vec_3d = D - A
        b_vec = np.array([b_vec_3d[0], b_vec_3d[1]])
        
        if abs(np.linalg.det(M_intersect)) > 0.001:
            solution = np.linalg.solve(M_intersect, b_vec)
            s_intersect = solution[0]
            L = A + s_intersect * perp_to_BC  # Point L on DE
        else:
            # Fallback: project A onto line DE
            L = D + np.dot(A - D, DE_vec) / np.dot(DE_vec, DE_vec) * DE_vec
        
        # Draw line AL (perpendicular to BC)
        line_AL = DashedLine(A, L, color=YELLOW, stroke_width=2)
        label_L = MathTex("L", color=YELLOW).scale(0.6).next_to(L, DOWN, buff=0.1)
        label_M = MathTex("M", color=YELLOW).scale(0.6).next_to(M, RIGHT, buff=0.1)
        
        # Add right angle marker at M
        right_angle_M = RightAngle(Line(M, B), Line(M, A), length=0.2, color=YELLOW)
        
        self.play(Create(line_AL))
        self.play(Write(label_L), Write(label_M), Create(right_angle_M))
        self.wait(1)
        
        # Create rectangles BDLM and CELM
        rect_BDLM = Polygon(B, D, L, M, color=ORANGE, fill_opacity=0.2, stroke_width=2)
        rect_CELM = Polygon(C, E, L, M, color=PURPLE, fill_opacity=0.2, stroke_width=2)
        
        self.play(
            FadeIn(rect_BDLM),
            FadeIn(rect_CELM),
            run_time=1
        )
        self.wait(1)
        
        # Now show the proof: Square ABFG = Rectangle BDLM
        # First, draw triangles ΔABD and ΔFBC
        
        # Draw line AD
        line_AD = Line(A, D, color=YELLOW, stroke_width=2)
        # Draw line FC
        line_FC = Line(F, C, color=YELLOW, stroke_width=2)
        
        # Create triangles
        triangle_ABD = Polygon(A, B, D, color=YELLOW, fill_opacity=0.2, stroke_width=2)
        triangle_FBC = Polygon(F, B, C, color=YELLOW, fill_opacity=0.2, stroke_width=2)
        
        self.play(
            Create(line_AD),
            Create(line_FC),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(triangle_ABD),
            FadeIn(triangle_FBC),
            run_time=1
        )
        self.wait(1)
        
        # Show that ΔABD ≅ ΔFBC (by SAS)
        # Highlight the congruent parts
        self.play(
            Indicate(triangle_ABD, color=YELLOW),
            Indicate(triangle_FBC, color=YELLOW),
            run_time=1.5
        )
        
        # Add text explaining congruence
        congruence1 = MathTex(r"\Delta ABD \cong \Delta FBC", color=YELLOW).scale(0.7)
        congruence1.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(congruence1))
        self.wait(1)
        
        # Show that Area(BDLM) = 2×Area(ΔABD) and Area(ABFG) = 2×Area(ΔFBC)
        # Since ΔABD ≅ ΔFBC, we get Area(BDLM) = Area(ABFG)
        self.play(
            Indicate(rect_BDLM, color=ORANGE),
            Indicate(triangle_ABD, color=YELLOW),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            Indicate(square_ABFG, color=BLUE),
            Indicate(triangle_FBC, color=YELLOW),
            run_time=1
        )
        self.wait(0.5)
        
        eq1 = MathTex(r"\text{Area}(BDLM) = \text{Area}(ABFG)", color=YELLOW).scale(0.7)
        eq1.next_to(congruence1, DOWN, buff=0.3)
        self.play(Write(eq1))
        self.wait(1)
        
        # Fade out first part
        self.play(
            FadeOut(triangle_ABD),
            FadeOut(triangle_FBC),
            FadeOut(line_AD),
            FadeOut(line_FC),
            FadeOut(congruence1),
            FadeOut(eq1)
        )
        self.wait(0.5)
        
        # Now show the second part: Square ACKH = Rectangle CELM
        # Draw triangles ΔACE and ΔKCB
        
        # Draw line AE
        line_AE = Line(A, E, color=YELLOW, stroke_width=2)
        # Draw line BK
        line_BK = Line(B, K, color=YELLOW, stroke_width=2)
        
        # Create triangles
        triangle_ACE = Polygon(A, C, E, color=YELLOW, fill_opacity=0.2, stroke_width=2)
        triangle_KCB = Polygon(K, C, B, color=YELLOW, fill_opacity=0.2, stroke_width=2)
        
        self.play(
            Create(line_AE),
            Create(line_BK),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(triangle_ACE),
            FadeIn(triangle_KCB),
            run_time=1
        )
        self.wait(1)
        
        # Show that ΔACE ≅ ΔKCB (by SAS)
        self.play(
            Indicate(triangle_ACE, color=YELLOW),
            Indicate(triangle_KCB, color=YELLOW),
            run_time=1.5
        )
        
        congruence2 = MathTex(r"\Delta ACE \cong \Delta KCB", color=YELLOW).scale(0.7)
        congruence2.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(congruence2))
        self.wait(1)
        
        # Show area relationships
        self.play(
            Indicate(rect_CELM, color=PURPLE),
            Indicate(triangle_ACE, color=YELLOW),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            Indicate(square_ACKH, color=GREEN),
            Indicate(triangle_KCB, color=YELLOW),
            run_time=1
        )
        self.wait(0.5)
        
        eq2 = MathTex(r"\text{Area}(CELM) = \text{Area}(ACKH)", color=YELLOW).scale(0.7)
        eq2.next_to(congruence2, DOWN, buff=0.3)
        self.play(Write(eq2))
        self.wait(1)
        
        # Fade out second part
        self.play(
            FadeOut(triangle_ACE),
            FadeOut(triangle_KCB),
            FadeOut(line_AE),
            FadeOut(line_BK),
            FadeOut(congruence2),
            FadeOut(eq2)
        )
        self.wait(0.5)
        
        # Final conclusion
        # Area(BCED) = Area(BDLM) + Area(CELM) = Area(ABFG) + Area(ACKH)
        
        # Show that rect_BDLM + rect_CELM = square_BCED
        self.play(
            Indicate(rect_BDLM, color=ORANGE),
            Indicate(rect_CELM, color=PURPLE),
            Indicate(square_BCED, color=RED),
            run_time=2
        )
        self.wait(1)
        
        conclusion = MathTex(
            r"\text{Area}(BCED) = \text{Area}(ABFG) + \text{Area}(ACKH)",
            color=YELLOW
        ).scale(0.9).to_edge(UP)
        
        self.play(Write(conclusion))
        self.wait(1)
        
        # Show the final theorem
        theorem = MathTex(
            r"BC^2 = AB^2 + AC^2",
            color=YELLOW
        ).scale(1.2).next_to(conclusion, DOWN, buff=0.5)
        
        self.play(Write(theorem))
        self.wait(1)
        
        # Final emphasis on all three squares
        self.play(
            Indicate(square_ABFG, color=BLUE),
            Indicate(square_ACKH, color=GREEN),
            Indicate(square_BCED, color=RED),
            run_time=2
        )
        
        self.wait(2)


if __name__ == "__main__":
    import subprocess
    import sys
    from pathlib import Path

    # Scene to run
    scene_name = "PythagoreanTheorem"
    
    # Get the path to this file
    this_file = Path(__file__).resolve()
    
    # Run manim command
    cmd = ["manim", "-pql", str(this_file), scene_name]
    subprocess.run(cmd)
