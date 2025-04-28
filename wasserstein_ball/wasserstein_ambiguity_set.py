from manim import *

class WassersteinAmbiguitySet(Scene):
    def construct(self):
        # Step 0: Write the function at the top
        title = MathTex(
            r"\max_{\mathbb{P} \in \mathcal{W}} \mathbb{E}_{\mathbb{P}}\left[l(x, \xi)\right]"
        ).to_edge(UP)
        self.play(Write(title))

        # Step 1: Draw the Wasserstein ball and setup
        center_point = Dot(color=BLUE)
        center_label = MathTex(r"\hat{\mathbb{P}}").next_to(center_point, DOWN)
        wasserstein_ball = Circle(radius=2, color=BLUE, fill_opacity=0.2)
        wasserstein_ball.move_to(center_point.get_center())
        wasserstein_label = MathTex(r"\mathcal{W}").next_to(wasserstein_ball, UP)

        wasserstein_group = VGroup(center_point, center_label, wasserstein_ball, wasserstein_label)

        radius_line = Line(center_point.get_center(), center_point.get_center() + 2 * RIGHT, color=BLUE)
        radius_label = MathTex(r"\rho").next_to(radius_line, UP)
        wasserstein_group.add(radius_line, radius_label)

        worst_case_point = Dot(color=RED).move_to(1 * UP)
        worst_case_label = MathTex(r"\mathbb{P}^*(x)").next_to(worst_case_point, RIGHT)
        wasserstein_group.add(worst_case_point, worst_case_label)

        wasserstein_group.shift(3 * LEFT)

        self.play(Create(wasserstein_ball), Write(wasserstein_label), FadeIn(center_point), Write(center_label))
        self.play(Create(radius_line), Write(radius_label))
        self.play(FadeIn(worst_case_point), Write(worst_case_label))

        # Step 2: Number line
        number_line = NumberLine(x_range=[-2, 2, 1], length=6).to_edge(DOWN)
        x_label = MathTex(r"x").next_to(number_line, RIGHT)
        self.play(Create(number_line), Write(x_label))

        x_ball = Dot(color=YELLOW).move_to(number_line.n2p(-1))
        self.play(FadeIn(x_ball))

        # Step 3: Updater for worst-case point
        def update_worst_case(mob):
            x_position = number_line.p2n(x_ball.get_center())
            theta = PI * (x_position + 1)
            radius = 1
            new_position = center_point.get_center() + \
                radius * np.cos(theta) * UP + \
                radius * np.sin(1.2 * theta) * LEFT
            mob.move_to(new_position)

        worst_case_point.add_updater(update_worst_case)

        # Step 4: Traced path
        red_path = TracedPath(worst_case_point.get_center, stroke_color=RED, stroke_width=2)
        self.add(red_path)

        # Step 5: Bullet points
        bullet_points = VGroup(
            Tex(r"$\bullet$ $\mathcal{W}$: Wasserstein ball with radius $\rho$ and center $\hat{\mathbb{P}}$", font_size=28),
            Tex(r"$\bullet$ $l$: loss function", font_size=28),
            Tex(r"$\bullet$ $x$: decision variable", font_size=28),
            Tex(r"$\bullet$ $\xi \sim \mathbb{P}$: random variable", font_size=28),
            Tex(r"$\bullet$ $\mathbb{P}^*(x)$: worst-case distribution given $x$", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        bullet_points.next_to(wasserstein_group, RIGHT, buff=1)
        bullet_points.shift(0.5 * UP)
        self.play(LaggedStartMap(FadeIn, bullet_points, shift=DOWN, lag_ratio=0.2))

        # Step 6: Animate x
        self.play(
            x_ball.animate.move_to(number_line.n2p(1)),
            run_time=8,
            rate_func=smooth
        )

        # --- Now transition to argmin formulation ---

        # 1. Move old title slightly to the right
        self.play(
            title.animate.shift(RIGHT * 2),
            run_time=1
        )

        # 2. Introduce x* = argmin_x in green in front
        argmin_part = MathTex(
            r"x^* = \arg\min_x",
            tex_to_color_map={"x^*": GREEN}
        ).next_to(title, LEFT, buff=0.3)  # Slightly close
        self.play(FadeIn(argmin_part))

        # 2. Add a new bullet point about x^* without moving the whole list
        new_bullet = Tex(r"$\bullet$ $x^*$: optimal decision", font_size=28)
        new_bullet.next_to(bullet_points[-1], DOWN, aligned_edge=LEFT, buff=0.3)  # only position relative to last bullet
        self.play(FadeIn(new_bullet, shift=DOWN))

        # 2. Move x_ball to somewhere near middle (say at x=0)
        self.play(
            x_ball.animate.move_to(number_line.n2p(0)),
            run_time=1.5
        )

        # 3. Change x_ball color to GREEN to represent x^*
        self.play(x_ball.animate.set_color(GREEN))

        # 4. Update x_label to x^*
        x_star_label = MathTex(r"x^*", color=GREEN).next_to(x_ball, UP)
        self.play(Write(x_star_label))

        # 5. Update worst-case distribution label
        self.play(FadeOut(worst_case_label))  # Fadeout old label first
        worst_case_label_new = MathTex(
            r"\mathbb{P}^*(x^*)",
            tex_to_color_map={
                r"\mathbb{P}^*": RED,
                r"x^*": GREEN
            }
        ).next_to(worst_case_point, RIGHT).shift(0.3 * DOWN)  # Move slightly down
        self.play(Write(worst_case_label_new))

        # Finish
        worst_case_point.clear_updaters()
        self.wait(2)