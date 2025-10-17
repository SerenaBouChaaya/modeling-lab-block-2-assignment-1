from manim import *
import numpy as np

# =====================================================================
# HOW TO OPEN (Manim Community v0.19, no LaTeX)
# ---------------------------------------------------------------------
# 1. Render in WebM:
# manim -ql --format=webm ./GroupC_Block3_assignment1/script.py MatrixRankGeometry
#
# 2. Convert WebM → MP4 (optional, for better compatibility):
#    ffmpeg -i "PATH/TO/MatrixRankGeometry.webm" \
#      -c:v libopenh264 -b:v 2M -pix_fmt yuv420p -movflags +faststart \
#      -c:a aac -b:a 128k "PATH/TO/MatrixRankGeometry.mp4"
#
# 
# 3. Open the resulting video:
#    macOS:   open -a "Google Chrome" PATH/TO/MatrixRankGeometry.webm
#    Windows: start PATH\TO\MatrixRankGeometry.webm
#    Linux:   xdg-open PATH/TO/MatrixRankGeometry.webm
#
# (Replace PATH/TO with the actual folder shown in the Manim render log.)
# =====================================================================



def make_matrix_box(vals, font_size=28, h_pad=0.25, v_pad=0.25, bracket_scale=1.0):
    """
    Construit une "matrice" avec uniquement des Text et des crochets tracés (pas de LaTeX).
    vals: liste de lignes, ex: [[2, 0], [0, 1]]
    """
    rows = []
    max_cols = max(len(r) for r in vals)

    
    for r in vals:
        row_items = [Text(str(x), font_size=font_size) for x in r]
        while len(row_items) < max_cols:
            row_items.append(Text("", font_size=font_size))  # pour aligner si tailles différentes
        for i in range(1, len(row_items)):
            row_items[i].next_to(row_items[i - 1], RIGHT, buff=h_pad)
        rows.append(VGroup(*row_items))

    for i in range(1, len(rows)):
        rows[i].next_to(rows[i - 1], DOWN, buff=v_pad)

    grid = VGroup(*rows)

    
    top_y = grid.get_top()[1]
    bot_y = grid.get_bottom()[1]
    left_x = grid.get_left()[0]
    right_x = grid.get_right()[0]

    brace_pad = 0.15 * bracket_scale
    cap = 0.25 * bracket_scale

    
    left_bracket = VGroup(
        Line([left_x - brace_pad, top_y, 0], [left_x - brace_pad, bot_y, 0]),
        Line([left_x - brace_pad, top_y, 0], [left_x - brace_pad + cap, top_y, 0]),
        Line([left_x - brace_pad, bot_y, 0], [left_x - brace_pad + cap, bot_y, 0]),
    )
    right_bracket = VGroup(
        Line([right_x + brace_pad, top_y, 0], [right_x + brace_pad, bot_y, 0]),
        Line([right_x + brace_pad - cap, top_y, 0], [right_x + brace_pad, top_y, 0]),
        Line([right_x + brace_pad - cap, bot_y, 0], [right_x + brace_pad, bot_y, 0]),
    )

    return VGroup(grid, left_bracket, right_bracket)


def make_bullets(lines, font_size=24, line_spacing=0.25, bullet="•"):
    """Liste à puces simple (sans BulletedList/LaTeX)."""
    items = []
    for s in lines:
        t = Text(f"{bullet} {s}", font_size=font_size)
        if items:
            t.next_to(items[-1], DOWN, buff=line_spacing, aligned_edge=LEFT)
        items.append(t)
    return VGroup(*items)



class MatrixRankGeometry(ThreeDScene):
    def construct(self):
        self.show_full_rank()
        self.show_rank_deficient()
        self.show_rank_deficient_3d()

    
    def show_full_rank(self):
        title = Text("Full Rank Matrix (rank = 2)", font_size=40).to_edge(UP)
        self.add(title)
        self.add_fixed_in_frame_mobjects(title)  # reste fixe à l’écran (HUD)

        matrix_box = make_matrix_box([[2, 0], [0, 1]], font_size=28).scale(0.9)
        matrix_box.move_to(LEFT * 4 + UP * 2)
        self.add_fixed_in_frame_mobjects(matrix_box)  # HUD pour rester net/visible

        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            axis_config={"color": GREY_A, "stroke_width": 2},
            tips=False,
        ).scale(1.5)
        axes.move_to(RIGHT * 2).set_z_index(1)

        v1 = Arrow(axes.c2p(0, 0), axes.c2p(2, 0), color=BLUE, buff=0).set_z_index(3)
        v2 = Arrow(axes.c2p(0, 0), axes.c2p(0, 1), color=RED, buff=0).set_z_index(3)
        v1_label = Text("v₁", font_size=20, color=BLUE).next_to(v1, DOWN)
        v2_label = Text("v₂", font_size=20, color=RED).next_to(v2, LEFT)
        for lbl in (v1_label, v2_label):
            lbl.add_background_rectangle(opacity=0.85, buff=0.06)
            lbl.set_z_index(5)

        region = Polygon(
            axes.c2p(0, 0), axes.c2p(2, 0), axes.c2p(2, 1), axes.c2p(0, 1),
            fill_color=YELLOW, fill_opacity=0.2, stroke_color=YELLOW, stroke_width=3,
        ).set_z_index(2)

        self.play(FadeIn(matrix_box))
        self.play(Create(axes))
        self.play(GrowArrow(v1), FadeIn(v1_label))
        self.play(GrowArrow(v2), FadeIn(v2_label))
        self.play(FadeIn(region))

        explanation = Text(
            "The columns are indepedent ⇒ they generate a 2D space (the plane).\n"
            "rank(A) = 2 = number of columns.",
            font_size=20,
        ).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)  
        self.play(Write(explanation))
        self.wait(2)

        self.play(FadeOut(Group(axes, v1, v2, v1_label, v2_label, region)))
        self.play(FadeOut(Group(title, matrix_box, explanation)))

   
    def show_rank_deficient(self):
        title = Text("Rank Deficient Matrix (rank = 1)", font_size=40).to_edge(UP)
        self.add(title)
        self.add_fixed_in_frame_mobjects(title)

        matrix_box = make_matrix_box([[2, 4], [1, 2]], font_size=28).scale(0.9)
        matrix_box.move_to(LEFT * 4 + UP * 2)
        self.add_fixed_in_frame_mobjects(matrix_box)

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 3, 1],
            axis_config={"color": GREY_A, "stroke_width": 2},
            tips=False,
        ).scale(1.5)
        axes.move_to(RIGHT * 2).set_z_index(1)

        v1 = Arrow(axes.c2p(0, 0), axes.c2p(2, 1), color=BLUE, buff=0).set_z_index(3)
        v2 = Arrow(axes.c2p(0, 0), axes.c2p(4, 2), color=RED, buff=0).set_z_index(3)
        v1_label = Text("v₁", font_size=20, color=BLUE).next_to(v1, DOWN)
        v2_label = Text("v₂ = 2·v₁", font_size=20, color=RED).next_to(v2, UP)
        for lbl in (v1_label, v2_label):
            lbl.add_background_rectangle(opacity=0.85, buff=0.06)
            lbl.set_z_index(5)

        line = Line(axes.c2p(-2, -1), axes.c2p(6, 3), color=YELLOW, stroke_width=3).set_z_index(2)

        self.play(FadeIn(matrix_box))
        self.play(Create(axes))
        self.play(GrowArrow(v1), FadeIn(v1_label))
        self.play(GrowArrow(v2), FadeIn(v2_label))
        self.play(Create(line))

        explanation = Text(
            "v₂ is a multiple of v₁ ⇒ linear dependence.\n"
            "Generated space = a 1D line.\n"
            "rank(A) = 1 < number of columns.",
            font_size=20,
        ).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)

        self.play(FadeOut(Group(axes, v1, v2, v1_label, v2_label, line)))
        self.play(FadeOut(Group(title, matrix_box, explanation)))

    
    def show_rank_deficient_3d(self):
        title = Text("Rank Deficient in 3D (rank = 2)", font_size=40).to_edge(UP)
        self.add(title)
        self.add_fixed_in_frame_mobjects(title)  # HUD

        matrix_box = make_matrix_box([[1, 0, 1], [0, 1, 1], [0, 0, 0]], font_size=24).scale(0.9)
        matrix_box.move_to(LEFT * 4 + UP * 2)
        self.add_fixed_in_frame_mobjects(matrix_box)  # HUD (reste net)

        axes = ThreeDAxes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            z_range=[-1, 1, 1],
            tips=False,
            axis_config={"stroke_width": 2},
        ).scale(1.2)
        axes.move_to(RIGHT * 2).set_z_index(1)

        
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        
        v1_3d = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(1, 0, 0), color=BLUE).set_z_index(3)
        v2_3d = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(0, 1, 0), color=RED).set_z_index(3)
        v3_3d = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(1, 1, 0), color=GREEN).set_z_index(3)

        
        v1_label = Text("v₁", font_size=22, color=BLUE).move_to(axes.c2p(1.1, 0, 0))
        v2_label = Text("v₂", font_size=22, color=RED).move_to(axes.c2p(0, 1.1, 0))
        v3_label = Text("v₃ = v₁ + v₂", font_size=22, color=GREEN).move_to(axes.c2p(1.1, 1.1, 0))
        self.add_fixed_orientation_mobjects(v1_label, v2_label, v3_label)
        for lbl in (v1_label, v2_label, v3_label):
            lbl.add_background_rectangle(opacity=0.85, buff=0.06)
            lbl.set_z_index(5)

        self.play(FadeIn(matrix_box))
        self.play(Create(axes))
        self.add(v1_3d); self.add(v2_3d); self.add(v3_3d)
        self.play(FadeIn(v1_label), FadeIn(v2_label), FadeIn(v3_label))

        # Plan xy en arrière-plan
        plane_pts = [axes.c2p(0, 0, 0), axes.c2p(2, 0, 0), axes.c2p(2, 2, 0), axes.c2p(0, 2, 0)]
        plane = Polygon(*plane_pts, fill_color=YELLOW, fill_opacity=0.12,
                        stroke_color=YELLOW, stroke_width=3).set_z_index(2)
        self.add(plane)

        explanation = Text(
            "3 ccolumns but v₃ = v₁ + v₂ ⇒ only 2 independent.\n"
            "All live in the xy plane.\n"
            "rank(A) = 2 < 3 columns.",
            font_size=18,
        ).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)  
        self.play(Write(explanation))
        self.wait(2)



