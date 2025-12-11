from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
        self.wait(1)

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI/4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

# class StickPerson(Scene):
#     def construct(self):
#         head = Circle(color=WHITE, radius=0.5,fill_opacity=0.5)
#         head.shift(UP*2)
#         body = Line(color=WHITE, width=1, height=2,fill_opacity=0.5)
#         body.shift(DOWN*0.5)
#         legs = Line(color=WHITE, start=body.get_center(), end=body.get_center()+DOWN)
#         legs.shift(DOWN*0.5)
#         self.play(Create(head))
#         self.play(Create(body))
#         self.play(Create(legs))
#         self.wait(1)

class StickPerson(Scene):
    def construct(self):
        # head
        head = Circle(color=WHITE, radius=0.65, fill_opacity=0.5)
        head.shift(UP * 2)

        # body
        body_start = head.get_bottom()
        body_end = body_start + DOWN * 2
        body = Line(body_start, body_end, color=WHITE)

        # legs
        left_leg = Line(body_end, body_end + DOWN * 1.5 + LEFT * 0.7, color=WHITE)
        right_leg = Line(body_end, body_end + DOWN * 1.5 + RIGHT * 0.7, color=WHITE)

        # arms
        left_arm = Line(body_start+DOWN*0.2, body_start + LEFT * 1+DOWN*1, color=WHITE)
        right_arm = Line(body_start+DOWN*0.2, body_start + RIGHT * 1+DOWN*1, color=WHITE)

        self.play(Create(head), Create(body), Create(left_leg), Create(right_leg), Create(left_arm), Create(right_arm))
        self.wait(1)


