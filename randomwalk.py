from manim import *
import random


class RandomWalk(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE},
            tips=True,
        )
        
        # Add coordinate numbers to axes
        axes.add_coordinates()
        
        # Add labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y", edge=LEFT, direction=LEFT)
        
        # Display axes
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # Parameters for the random walk
        num_steps = 8  # Number of steps in x direction
        step_size = 1.0  # Step size in x and y
        
        # Generate all possible paths (binary tree)
        # Each path is a sequence of up/down moves
        all_paths = []
        
        def generate_paths(steps):
            """Generate all 2^steps possible paths"""
            if steps == 0:
                return [[]]
            shorter_paths = generate_paths(steps - 1)
            return [path + [1] for path in shorter_paths] + [path + [-1] for path in shorter_paths]
        
        all_paths = generate_paths(num_steps)
        
        # Create lines step by step, spreading out based on x
        # We'll build the tree level by level (x by x)
        
        # Store all line segments grouped by x-step
        step_segments = [VGroup() for _ in range(num_steps)]
        all_segments = VGroup()  # Container for all segments
        
        # Build the segments for each path
        for path in all_paths:
            x = 0
            y = 0
            
            for step_idx, direction in enumerate(path):
                start_point = axes.c2p(x, y)
                x += step_size
                y += direction * step_size
                end_point = axes.c2p(x, y)
                
                # Create a line segment for this step
                segment = Line(start_point, end_point)
                segment.set_stroke(GRAY, width=1, opacity=0.3)
                step_segments[step_idx].add(segment)
        
        # Animate each x-step appearing simultaneously
        for step_group in step_segments:
            self.play(Create(step_group, lag_ratio=0), run_time=0.4)
            all_segments.add(step_group)  # Add to master group
        
        self.wait(0.5)
        
        # Choose one random path to highlight
        chosen_path_index = random.randint(0, len(all_paths) - 1)
        chosen_path = all_paths[chosen_path_index]
        
        # Create the highlighted path
        points = [axes.c2p(0, 0)]
        x = 0
        y = 0
        
        for direction in chosen_path:
            x += step_size
            y += direction * step_size
            points.append(axes.c2p(x, y))
        
        highlighted_path = VMobject()
        highlighted_path.set_points_as_corners(points)
        highlighted_path.set_stroke(BLUE, width=4)
        
        # Add a dot to trace along the path
        dot = Dot(axes.c2p(0, 0), color=BLUE, radius=0.08)
        
        # Animate the highlighted path being traced
        self.play(Create(dot))
        self.bring_to_front(dot)  # Keep dot in front of the path
        self.play(
            Create(highlighted_path),
            MoveAlongPath(dot, highlighted_path),
            run_time=4,
            rate_func=linear
        )
        
        self.wait(1)
        
        # Fade out the branching paths and dot
        self.play(
            FadeOut(all_segments),
            FadeOut(dot),
            run_time=1
        )
        
        self.wait(0.5)
        
        # Generate additional steps for the continuation (500 more steps)
        additional_steps = 500
        continuation_path = [random.choice([1, -1]) for _ in range(additional_steps)]
        
        # Calculate the full walk (first 8 steps + 500 additional steps)
        total_steps = num_steps + additional_steps
        full_path = chosen_path + continuation_path
        
        # Calculate the y range for the full walk
        y = 0
        min_y = 0
        max_y = 0
        
        for direction in full_path:
            y += direction * step_size
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        
        # Create buffer for y range
        y_range_buffer = max(abs(min_y), abs(max_y)) * 1.2
        
        # Create new axes that show the full walk with smaller step size
        new_axes = Axes(
            x_range=[0, total_steps, 50],
            y_range=[-y_range_buffer, y_range_buffer, max(10, int(y_range_buffer/5))],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE},
            tips=True,
        )
        
        # Add coordinate numbers to new axes
        new_axes.add_coordinates()
        
        new_x_label = new_axes.get_x_axis_label("x")
        new_y_label = new_axes.get_y_axis_label("y", edge=LEFT, direction=LEFT)
        
        # Recreate the first walk on the new axes (compressed)
        compressed_points = [new_axes.c2p(0, 0)]
        x = 0
        y = 0
        
        for direction in chosen_path:
            x += step_size
            y += direction * step_size
            compressed_points.append(new_axes.c2p(x, y))
        
        compressed_path = VMobject()
        compressed_path.set_points_as_corners(compressed_points)
        compressed_path.set_stroke(BLUE, width=4)
        
        # Transform the old axes to new axes and compress the highlighted path
        self.play(
            Transform(axes, new_axes),
            Transform(x_label, new_x_label),
            Transform(y_label, new_y_label),
            Transform(highlighted_path, compressed_path),
            run_time=2
        )
        
        self.wait(0.5)
        
      
        
        # Create the continuation path (starts from where first walk ended)
        continuation_points = [new_axes.c2p(num_steps, y)]  # Start from end of first walk
        x = num_steps
        # y is already at the correct value from the loop above
        
        for direction in continuation_path:
            x += step_size
            y += direction * step_size
            continuation_points.append(new_axes.c2p(x, y))
        
        continuation_line = VMobject()
        continuation_line.set_points_as_corners(continuation_points)
        continuation_line.set_stroke(BLUE, width=2)
        
        # Draw the continuation (still in blue)
        # Start dot at the end of the first walk
        continuation_dot = Dot(new_axes.c2p(num_steps, sum([d * step_size for d in chosen_path])), 
                               color=BLUE, radius=0.06)
        self.play(Create(continuation_dot))
        self.bring_to_front(continuation_dot)  # Keep dot in front of the path
        self.play(
            Create(continuation_line),
            MoveAlongPath(continuation_dot, continuation_line),
            run_time=6,
            rate_func=linear
        )
        
        self.wait(0.5)


        
        # Adding y=x and y=-x reference lines
        # Use visible range for x_range
        max_visible_x = min(total_steps, y_range_buffer)
        y_equals_x = new_axes.plot(lambda x: x, x_range=[0, max_visible_x], color=YELLOW, stroke_width=2)
        y_equals_neg_x = new_axes.plot(lambda x: -x, x_range=[0, max_visible_x], color=YELLOW, stroke_width=2)
        
        # Add labels for the lines - position at specific coordinates
        label_x_pos = 40
        label_y_pos = 17
        
        y_x_label = MathTex("y=x", color=YELLOW).scale(0.6)
        y_x_label.next_to(new_axes.c2p(label_x_pos, label_y_pos), UP)
        
        y_neg_x_label = MathTex("y=-x", color=YELLOW).scale(0.6)
        y_neg_x_label.next_to(new_axes.c2p(label_x_pos, -label_y_pos), DOWN)
        y_neg_x_label.shift(RIGHT * 0.3)  # Shift right
        
        # Show the reference lines - draw graphs first
        self.play(
            Create(y_equals_x),
            Create(y_equals_neg_x),
            run_time=1.5
        )
        # Then write the labels
        self.play(
            Write(y_x_label),
            Write(y_neg_x_label),
            run_time=1.5
        )
        
        # Adding y=x^0.5 and y=-x^0.5 reference lines
        y_equals_sqrt_x = new_axes.plot(lambda x: x**0.5, x_range=[0, 500], color=PINK, stroke_width=2)
        y_equals_neg_sqrt_x = new_axes.plot(lambda x: -(x**0.5), x_range=[0, 500], color=PINK, stroke_width=2)
        
        # Add labels for the sqrt lines
        sqrt_label_x_pos = 200
        sqrt_label_y_pos = 17
        
        y_sqrt_x_label = MathTex("y=x^{0.5}", color=PINK).scale(0.6)
        y_sqrt_x_label.next_to(new_axes.c2p(sqrt_label_x_pos, sqrt_label_y_pos), UP)
        
        y_neg_sqrt_x_label = MathTex("y=-x^{0.5}", color=PINK).scale(0.6)
        y_neg_sqrt_x_label.next_to(new_axes.c2p(sqrt_label_x_pos, -sqrt_label_y_pos), DOWN)
        
        # Show the sqrt reference lines - draw graphs first
        self.play(
            Create(y_equals_sqrt_x),
            Create(y_equals_neg_sqrt_x),
            run_time=1.5
        )
        # Then write the labels
        self.play(
            Write(y_sqrt_x_label),
            Write(y_neg_sqrt_x_label),
            run_time=1.5
        )
        
        # Shade the area between the pink lines
        # Create filled area between y=x^0.5 and y=-x^0.5
        # Generate points along both curves
        num_points = 100
        area_points = []
        
        # Points along the upper curve (y=x^0.5) from right to left
        for i in range(num_points, -1, -1):
            x = 500 * (i / num_points)
            y = x**0.5
            area_points.append(new_axes.c2p(x, y))
        
        # Points along the lower curve (y=-x^0.5) from left to right
        for i in range(num_points + 1):
            x = 500 * (i / num_points)
            y = -(x**0.5)
            area_points.append(new_axes.c2p(x, y))
        
        # Close the polygon
        area_points.append(area_points[0])
        
        # Create filled polygon
        filled_area = Polygon(*area_points, fill_opacity=0.3, fill_color=PINK, stroke_width=0)
        
        # Animate the shading
        self.play(FadeIn(filled_area), run_time=1.5)

        # Final pause
        self.wait(2)




if __name__ == "__main__":
    import subprocess
    import sys
    from pathlib import Path

    # Scene to run
    scene_name = "RandomWalk"
    
    # Get the path to this file
    this_file = Path(__file__).resolve()
    
    # Run manim command
    cmd = ["manim", "-pql", str(this_file), scene_name]
    subprocess.run(cmd)
