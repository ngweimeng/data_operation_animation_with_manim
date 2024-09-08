from manim import *

class DataMelt(Scene):
    def construct(self):

        # -----Functions-----
        def create_subtitle(text):
            subtitle = Text(text).scale(0.5).to_edge(DOWN, buff=0.4)
            return subtitle

        def create_console(x, y, z, color_fill, code_text):
            console_rect = Rectangle(width=x, height=y, stroke_width=1, fill_color=color_fill).set_fill(color_fill, 0.5).shift(z)
            red_arrow_text = MarkupText(r'>>> ', color=RED_D, opacity=1).scale(0.45).next_to(console_rect.get_left(), RIGHT, buff=0.3)
            code_text = Text(code_text, color=WHITE, opacity=1).scale(0.45).next_to(red_arrow_text, RIGHT, buff=0.1)
            return VGroup(console_rect, red_arrow_text, code_text)

        def create_dataframe(headers, data, pos_shift):
            header_row = create_row([f'<b>{header}</b>' for header in headers], pos_shift, fill_color=GREY_D)
            rows = [header_row]
            for i, row_data in enumerate(data):
                y_shift = pos_shift - (i + 1) * 0.35 * UP
                rows.append(create_row(row_data, y_shift))
            return rows

        def create_row(texts, y_shift, fill_color=None):
            row = []
            previous_table = None
            for text in texts:
                table = create_cell(f'<span font_family="monospace">{text}</span>', fill_color)
                if previous_table is None:
                    table.shift(y_shift + 4.5 * LEFT)
                else:
                    table.next_to(previous_table, RIGHT, buff=0) 
                row.append(table)
                previous_table = table
            return row

        def create_cell(text, fill_color=None):
            cell = Rectangle(width=3, height=0.6)
            cell.set_stroke(color=GREY, opacity=1).scale(0.6)
            if fill_color:
                cell.set_fill(fill_color, opacity=1)
            text = MarkupText(text).scale(0.4)
            return VGroup(cell, text)

        def create_index_column(indices, data_rows):
            index_column = []
            for i, index_value in enumerate(indices):
                index = MarkupText(
                    f'<span font_family="monospace"><b>{index_value}</b></span>',
                    color=GREY_A,
                    opacity=1
                ).scale(0.45)
                index.next_to(data_rows[i][0].get_left(), LEFT, buff=0.2)
                index_column.append(index)
            return index_column

        def highlight_rows(rows, columns, color):
            highlights = []
            for row in rows:
                for i in columns:
                    highlight = create_highlight(3, 0.6, color).move_to(row[i].get_center())
                    highlights.append(highlight)
            return highlights
        
        def create_highlight(x, y, color):
            return Rectangle(width=x, height=y).set_stroke(color=color, opacity=1).set_fill(color=color, opacity=0.5).scale(0.6)

        # -----Title-----
        title = MarkupText('Data Melting', color=GOLD).scale(0.7).shift(3.5 * UP)
        self.play(FadeIn(title))

        # -----Original DataFrame-----
        headers = ["Name", "Age", "Math", "Science"]
        data = [
            ["Alice", "28", "85", "90"],
            ["Bob", "34", "75", "85"],
            ["Charlie", "25", "95", "89"]
        ]

        dataframe_rows = create_dataframe(headers, data, 2.3 * UP)
        index_column_1 = create_index_column([str(i) for i in range(3)], dataframe_rows[1:])

        subtitle_1 = create_subtitle("Here is the initial Dataframe, 'df' with students' scores in different subjects.")
        console_1 = create_console(13.9, 0.6, 2.9 * UP, DARK_GREY, 'df')

        self.add(subtitle_1)
        self.play(FadeIn(console_1), *[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
        self.wait(1)
        self.play(FadeOut(subtitle_1))

        # -----Melt Transformation-----
        subtitle_2 = create_subtitle("Now, we'll melt the DataFrame, which means turning columns into rows.")
        self.play(FadeIn(subtitle_2))
        console_2 = create_console(13.9, 0.6, 0 * DOWN, DARK_GREY, 'df.melt(id_vars=["Name", "Age"], var_name="Subject", value_name="Score")')
        self.play(FadeIn(console_2))
        self.wait(1)
        self.play(FadeOut(subtitle_2))

        subtitle_4 = create_subtitle("In melting, we keep 'Name' and 'Age' intact, while converting subject scores into rows.")
        self.play(FadeIn(subtitle_4))
        self.wait(1)
        highlight_rectangles_alice = highlight_rows([dataframe_rows[i] for i in [1]], range(2, 4), YELLOW)
        highlight_rectangles_bob = highlight_rows([dataframe_rows[i] for i in [2]], range(2, 4), BLUE)
        highlight_rectangles_charlie = highlight_rows([dataframe_rows[i] for i in [3]], range(2, 4), RED)
        self.play(*[Create(highlight) for highlight in highlight_rectangles_alice])
        self.play(*[Create(highlight) for highlight in highlight_rectangles_bob])
        self.play(*[Create(highlight) for highlight in highlight_rectangles_charlie])

        # Melted DataFrame
        melted_headers = ["Name", "Age", "Subject", "Score"]
        melted_data = [
            ["Alice", "28", "Math", "85"],
            ["Alice", "28", "Science", "90"],
            ["Bob", "34", "Math", "75"],
            ["Bob", "34", "Science", "85"],
            ["Charlie", "25", "Math", "95"],
            ["Charlie", "25", "Science", "89"],
        ]

        melted_dataframe_rows = create_dataframe(melted_headers, melted_data, -0.6 * UP)
        filtered_index_column = create_index_column(["0", "1", "2", "3", "4", "5"], melted_dataframe_rows[1:])

        highlight_rectangles_alice_res = highlight_rows([melted_dataframe_rows[i] for i in [1,2]], range(3, 4), YELLOW)
        highlight_rectangles_bob_res = highlight_rows([melted_dataframe_rows[i] for i in [3,4]], range(3, 4), BLUE)
        highlight_rectangles_charlie_res = highlight_rows([melted_dataframe_rows[i] for i in [5,6]], range(3, 4), RED)

        self.play(FadeIn(VGroup(*melted_dataframe_rows[0]))) 

        alice_transform = [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in melted_dataframe_rows[1:3] for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in highlight_rectangles_alice_res for cell in row]))
        ]
        self.play(AnimationGroup(*alice_transform, lag_ratio=0), run_time=1.75)

        bob_transform = [
            TransformFromCopy(Group(*highlight_rectangles_bob), Group(*[cell for row in melted_dataframe_rows[3:5] for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_bob), Group(*[cell for row in highlight_rectangles_bob_res for cell in row]))
        ]
        self.play(AnimationGroup(*bob_transform, lag_ratio=0), run_time=1.75)

        charlie_transform = [
            TransformFromCopy(Group(*highlight_rectangles_charlie), Group(*[cell for row in melted_dataframe_rows[5:7] for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_charlie), Group(*[cell for row in highlight_rectangles_charlie_res for cell in row]))
        ]
        self.play(AnimationGroup(*charlie_transform, lag_ratio=0), run_time=1.75)

        self.play(*[FadeIn(index) for index in filtered_index_column])
        self.play(FadeOut(subtitle_4))

        subtitle_5 = create_subtitle("The melted DataFrame has 'Subject' as a new column and scores as values.")
        self.play(FadeIn(subtitle_5))
        self.wait(2)