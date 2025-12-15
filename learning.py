from manim import *


# class CreateCircle(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
#         self.play(Create(circle))  # show the circle on screen
#         self.wait(1)

# class SquareToCircle(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         circle.set_fill(PINK, opacity=0.5)  # set color and transparency

#         square = Square()  # create a square
#         square.rotate(PI/4)  # rotate a certain amount

#         self.play(Create(square))  # animate the creation of the square
#         self.play(Transform(square, circle))  # interpolate the square into the circle
#         self.play(FadeOut(square))  # fade out animation

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
        head = Circle(color=WHITE, radius=0.65)
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

        stick_person = VGroup(head, body, left_leg, right_leg, left_arm, right_arm) #Ordered list of mobjects, animates one after the other

        self.play(Create(stick_person, lag_ratio=0.5)) # can add lag_ratio to control the speed of the animation
        self.play(head.animate.set_fill(WHITE, opacity=0.5))  # color the circle on screen
        self.play(stick_person.animate.rotate(PI), run_time=1) #.rotate only interpoloates the start and ending state
        self.wait(0.5)
        self.play(Rotate(stick_person, angle=PI), run_time=1)  #Rotate() actually rotates the object
        
        # Transform head into square, then triangle
        b = Square(color=WHITE, fill_opacity=0.5)
        # Position square so its bottom aligns with top of body (body_start)
        b.move_to(body_start + UP * (b.get_height() / 2))
        c = Triangle(color=WHITE, fill_opacity=0.5)
        # Position triangle so its bottom aligns with top of body (body_start)
        c.move_to(body_start + UP * (c.get_height() / 2))        
        self.play(Transform(head, b))
        self.play(Transform(head, c))
        self.play(FadeOut(head))





# class TwoTransforms(Scene):
#     def transform(self):
#         a = Circle()
#         b = Square()
#         c = Triangle()
#         self.play(Transform(a, b))
#         self.play(Transform(a, c))
#         self.play(FadeOut(a))

#     def replacement_transform(self):
#         a = Circle()
#         b = Square()
#         c = Triangle()
#         self.play(ReplacementTransform(a, b))
#         self.play(ReplacementTransform(b, c))
#         self.play(FadeOut(c))

#     def construct(self):
#         self.transform()
#         self.wait(0.5)  # wait for 0.5 seconds
#         self.replacement_transform()




if __name__ == "__main__":
    import subprocess
    import sys
    from pathlib import Path

    # Default scene to run (change this to run a different scene)
    scene_name = "StickPerson"
    
    # Get the path to this file
    this_file = Path(__file__).resolve()
    
    # Run manim command
    cmd = ["manim", "-pql", str(this_file), scene_name]
    subprocess.run(cmd)