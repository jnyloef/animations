from manim import *

class WassersteinAmbiguitySet(Scene):
    def construct(self):
        #self.camera.background_color = WHITE

        # Step 0: Write the function at the top
        title = MathTex(
            r"\max_{\mathbb{P} \in \mathcal{W}} \mathbb{E}_{\mathbb{P}}\left[l(x, \xi)\right]"
        ).to_edge(UP)
        self.play(Write(title))

        # Step 1: Draw the Wasserstein ball
        center_point = Dot(color=BLUE)
        center_label = MathTex(r"\hat{\mathbb{P}}").next_to(center_point, DOWN)
        wasserstein_ball = Circle(radius=2, color=BLUE, fill_opacity=0.2)
        wasserstein_ball.move_to(center_point.get_center())
        wasserstein_label = MathTex(r"\mathcal{W}").next_to(wasserstein_ball, UP)

        # Group the ball components together
        wasserstein_group = VGroup(center_point, center_label, wasserstein_ball, wasserstein_label)

        # Step 2: Mark the radius as \rho
        radius_line = Line(center_point.get_center(), center_point.get_center() + 2 * RIGHT, color=BLUE)
        radius_label = MathTex(r"\rho").next_to(radius_line, UP)
        wasserstein_group.add(radius_line, radius_label)

        # Step 3: Add the worst-case distribution point
        worst_case_point = Dot(color=RED).move_to(1 * UP)
        worst_case_label = MathTex(r"\mathbb{P}^*(x)").next_to(worst_case_point, RIGHT)
        wasserstein_group.add(worst_case_point, worst_case_label)

        # Shift the whole Wasserstein group a bit left
        wasserstein_group.shift(3 * LEFT)

        # Play creation animations
        self.play(Create(wasserstein_ball), Write(wasserstein_label), FadeIn(center_point), Write(center_label))
        self.play(Create(radius_line), Write(radius_label))
        self.play(FadeIn(worst_case_point), Write(worst_case_label))

        # Step 4: Draw a number line for x
        number_line = NumberLine(x_range=[-2, 2, 1], length=6).to_edge(DOWN)
        x_label = MathTex(r"x").next_to(number_line, RIGHT)
        self.play(Create(number_line), Write(x_label))

        # Add a ball representing x on the number line
        x_ball = Dot(color=YELLOW).move_to(number_line.n2p(-1))  # Start at x = -1
        self.play(FadeIn(x_ball))

        # Step 5: Make the worst_case_point move depending on x_ball
        def update_worst_case(mob):
            x_position = number_line.p2n(x_ball.get_center())
            theta = PI * (x_position + 1)  # map x from [-1,1] to [0,2pi]
            radius = 1
            new_position = center_point.get_center() + \
                radius * np.cos(theta) * UP + \
                radius * np.sin(1.2 * theta) * LEFT
            mob.move_to(new_position)

        worst_case_point.add_updater(update_worst_case)

        # Add a trajectory trace for the red point
        red_path = TracedPath(worst_case_point.get_center, stroke_color=RED, stroke_width=2)
        self.add(red_path)

        # Step 6: Add bullet point list on the right
        bullet_points = VGroup(
            Tex(r"$\bullet$ $\mathcal{W}$: Wasserstein ball with radius $\rho$ and center $\hat{\mathbb{P}}$", font_size=28),
            Tex(r"$\bullet$ $l$: loss function", font_size=28),
            Tex(r"$\bullet$ $x$: decision variable", font_size=28),
            Tex(r"$\bullet$ $\xi \sim \mathbb{P}$: random variable", font_size=28),
            Tex(r"$\bullet$ $\mathbb{P}^*(x)$: worst-case distribution given $x$", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        bullet_points.next_to(wasserstein_group, RIGHT, buff=1)  # to the right of the ball
        bullet_points.shift(0.5 * UP)  # shift slightly up for better centering

        self.play(LaggedStartMap(FadeIn, bullet_points, shift=DOWN, lag_ratio=0.2))

        # Step 7: Animate the yellow ball moving
        self.play(
            x_ball.animate.move_to(number_line.n2p(1)),  # Move x_ball from x = -1 to x = 1
            run_time=10,
            rate_func=smooth
        )

        # After animation, remove the updater
        worst_case_point.clear_updaters()

        self.wait(2)

