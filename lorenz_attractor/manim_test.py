from manim import *
import numpy as np

class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up the axes
        axes = ThreeDAxes(
            x_range=[-50, 50, 10],  # Increased range for better visibility
            y_range=[-50, 50, 10],
            z_range=[0, 50, 10],   # Increased z-range for better visibility
            x_length=10,
            y_length=10,
            z_length=5,
        )
        # Zoom out the camera by increasing the frame width
        self.camera.frame_center = [0, 1.4, 0]  # Shift the origin down by 2 units
        self.set_camera_orientation(
            phi=70 * DEGREES,  # Adjust the vertical angle
            theta=-45 * DEGREES,  # Adjust the horizontal angle
            zoom=0.9  # Zoom out to fit the entire scene
        )
        self.add(axes)

        # Parameters for the Lorenz system
        sigma = 10
        rho = 28
        beta = 8 / 3

        # Initial conditions
        dt = 0.01
        num_points = 1000
        x, y, z = 0.1, 0.1, 0.1

        # Generate points for the Lorenz attractor
        points = []
        for _ in range(num_points):
            dx = sigma * (y - x) * dt
            dy = (x * (rho - z) - y) * dt
            dz = (x * y - beta * z) * dt
            x += dx
            y += dy
            z += dz
            points.append(axes.c2p(x, y, z))  # c2p = convert to 3D coordinates

        # Create a ball that moves along the attractor
        ball = Sphere(radius=0.1, color=RED).move_to(points[0])
        self.add(ball)

        # Create a VMobject to represent the path
        path = VMobject(color=BLUE, stroke_width=2)
        path.set_points_as_corners([points[0]])  # Start with the first point
        self.add(path)

        # Animate the ball moving along the attractor and draw the path
        def update_path(path):
            # Dynamically update the path with a smooth curve
            new_point = ball.get_center()
            path.add_points_as_corners([new_point])

        path.add_updater(update_path)

        # Add a traced path for the ball
        traced_path = TracedPath(ball.get_center, stroke_color=BLUE, stroke_width=2)
        self.add(traced_path)

        # Create a smooth attractor path for the ball to follow
        attractor = VMobject()
        attractor.set_points_smoothly(points)
        self.play(
            MoveAlongPath(ball, attractor, rate_func=linear, run_time=100)  # Rate function smooth makes it slow in the beginning and at the end
        )
        path.remove_updater(update_path)

        self.wait(2)