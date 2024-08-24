from manim import *

class Filtering(Scene):
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
        title = MarkupText('Filtering out NULL Values', color=GOLD).scale(0.7).shift(3.5 * UP)
        self.play(FadeIn(title))

        # -----Original DataFrame-----
        headers = ["Name", "Age", "Gender", "Title", "Salary", "Experience"]
        data = [
            ["Alice", "28", "Female", "Engineer", "85000", "5"],
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Charlie", "25", "Male", "Designer", "55000", "2"],
            ["Diana", "40", "Female", "Manager", "105000", "10"],
            ["Eve", "30", "", "Designer", "90000", "4"],
            ["Frank", "", "Male", "Engineer", "84000", "3"],
        ]

        dataframe_rows = create_dataframe(headers, data, 2.3 * UP)
        index_column_1 = create_index_column(["0", "1", "2", "3", "4", "5"], dataframe_rows[1:])

        subtitle_1 = create_subtitle("Here is the initial DataFrame, 'df', which contains some missing (null) values.")
        console_1 = create_console(13.9, 0.6, 2.9 * UP, DARK_GREY, 'df')

        # Highlight Null Values
        null_highlights = []
        null_highlights.append(create_highlight(3, 0.6, RED).move_to(dataframe_rows[6][1].get_center()))  # Frank's Age is NULL
        null_highlights.append(create_highlight(3, 0.6, RED).move_to(dataframe_rows[5][2].get_center()))  # Eve's Gender is NULL

        self.add(subtitle_1)
        self.play(FadeIn(console_1), *[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
        self.play(*[Create(highlight) for highlight in null_highlights])
        self.wait(1)
        self.play(FadeOut(subtitle_1))

        # -----Resultant Dataframe: Filter Null Values-----
        subtitle_2 = create_subtitle("Next, we filter the DataFrame to display only rows where all values are non-null.")
        console_2 = create_console(13.9, 0.6, 0.6 * DOWN, DARK_GREY, 'df.dropna()')

        self.add(subtitle_2)
        self.play(FadeIn(console_2))
        self.wait(1)

        highlight_rectangles = highlight_rows([dataframe_rows[i] for i in [1, 2, 3, 4]], range(6), YELLOW)
        self.play(*[Create(highlight) for highlight in highlight_rectangles])

        # Resultant DataFrame
        filtered_data = [
            ["Alice", "28", "Female", "Engineer", "85000", "5"],
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Charlie", "25", "Male", "Designer", "55000", "2"],
            ["Diana", "40", "Female", "Manager", "105000", "10"],
        ]

        filtered_rows = create_dataframe(headers, filtered_data, -1.2 * UP)
        filtered_index_column = create_index_column(["0", "1", "2", "3"], filtered_rows[1:])

        self.play(FadeIn(VGroup(*filtered_rows[0]))) 
        for original_row, new_row in zip([dataframe_rows[i] for i in [1, 2, 3, 4]], filtered_rows[1:]):
            self.play(*[TransformFromCopy(orig_cell, new_cell) for orig_cell, new_cell in zip(original_row, new_row)], run_time=1.75)
        self.play(*[FadeIn(index) for index in filtered_index_column])
        self.wait(1)
