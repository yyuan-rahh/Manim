from manim import *

class SimpleDemo(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))
        
        square = Square()
        square.next_to(circle, RIGHT)
        self.play(Create(square))
        
        text = Text("Manim Demo")
        text.next_to(VGroup(circle, square), UP)
        self.play(Write(text))
        self.wait()
