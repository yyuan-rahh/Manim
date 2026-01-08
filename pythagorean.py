from manim import *
import numpy as np

class righttriangle(Scene):
    def construct(self):
        # Zoom out to fit everything on screen
        self.camera.frame_width = 20
        self.camera.frame_height = 12
        
        p1 = [-2.5, -1.2, 0]
        p2 = [2.5, -1.2, 0]
        p3 = [-0.7, 1.2, 0]

        # Create the triangle using the Polygon mobject
        triangle = Polygon(p1, p2, p3, color=WHITE, stroke_width=2)
        
        # Create the lines forming the right angle
        line1 = Line(p1, p3)
        line2 = Line(p2, p3)
        
        # Create the right angle indicator
        right_angle = RightAngle(line1, line2, length=0.4, quadrant=(-1,-1)) # Adjust length/quadrant as needed
        
        self.play(Create(triangle))
        self.wait(0.5)
        self.play(Create(right_angle))
        self.wait(0.5)
        
        # Add squares to each side (enter side lengths manually)
        square1 = self.square_on_side(p1, p2, p3, 5.0, BLUE)  # length of side p1-p2
        square2 = self.square_on_side(p2, p3, p1, 4, PINK)  # length of side p2-p3
        square3 = self.square_on_side(p3, p1, p2, 3, GREEN)  # length of side p3-p1
        
        self.play(Create(square1), Create(square2), Create(square3), run_time=1.5)
        self.wait(2)
    
    def square_on_side(self, a, b, c, length, color):
        """Create a square on side ab, positioned outside the triangle"""
        square = Square(side_length=length, color=color, stroke_width=2, fill_opacity=0.5)
        mid = (np.array(a) + np.array(b)) / 2
        perp = np.array([-(b[1]-a[1]), b[0]-a[0], 0]) / np.linalg.norm(np.array(b) - np.array(a))
        if np.dot(np.array(c) - mid, perp) > 0:
            perp = -perp
        square.move_to(mid + perp * length/2)
        square.rotate(np.arctan2(b[1]-a[1], b[0]-a[0]), about_point=square.get_center())
        return square

