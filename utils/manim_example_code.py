example_code = """
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class Filtering(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com", global_speed=1.5))

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
            # Create the header row
            header_row = create_row([f'<b>{header}</b>' for header in headers], pos_shift)
            
            # Create the data rows
            rows = [header_row]
            for i, row_data in enumerate(data):
                y_shift = pos_shift - (i + 1) * 0.35 * UP
                rows.append(create_row(row_data, y_shift))
            
            return rows

        def create_row(texts, y_shift):
            row = []
            previous_table = None
            for text in texts:
                table = create_cell(f'<span font_family="monospace">{text}</span>')
                if previous_table is None:
                    table.shift(y_shift + 4.5 * LEFT)
                else:
                    table.next_to(previous_table, RIGHT, buff=0)  # No buffer between cells
                row.append(table)
                previous_table = table
            return row

        def create_cell(text):
            cell = Rectangle(width=3, height=0.6)
            cell.set_stroke(color=GREY, opacity=1).scale(0.6)
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
        title = MarkupText('Filtering with Python', opacity=1).scale(0.5).shift(3.65 * UP)
        self.play(FadeIn(title))

        # -----Original DataFrame-----
        headers = ["Name", "Age", "Gender", "Title", "Salary", "Experience"]
        data = [
            ["Alice", "28", "Female", "Engineer", "85000", "5"],
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Charlie", "25", "Male", "Designer", "55000", "2"],
            ["Diana", "40", "Female", "Manager", "105000", "10"],
            ["Eve", "30", "Female", "Designer", "90000", "4"],
            ["Frank", "29", "Male", "Engineer", "84000", "3"],
        ]

        dataframe_rows = create_dataframe(headers, data, 2.5 * UP)
        index_column_1 = create_index_column(["0", "1", "2", "3", "4", "5"], dataframe_rows[1:])

        subtitle_1 = create_subtitle("This is our DataFrame named 'employee_df'.")
        console_1 = create_console(13.9, 0.6, 3.1 * UP, DARK_GREY, 'employee_df')

        with self.voiceover(text="This is our DataFrame named 'employee_df'.") as tracker:
            self.add(subtitle_1)
            self.play(GrowFromCenter(console_1[0]), run_time=1)
            self.play(Write(console_1[1]), run_time=1)
            self.play(Write(console_1[2]), run_time=1)
            self.play(*[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
        self.play(FadeOut(subtitle_1))

        # -----Resultant Dataframe 1: Filter using "=="-----
        subtitle_2 = create_subtitle("Let's apply a filter to select employees whose Title is 'Engineer'.\nWe use a Boolean indexing method to achieve this.")
        console_2 = create_console(13.9, 0.6, 0.4 * DOWN, DARK_GREY, 'employee_df[employee_df["Title"] == "Engineer"]')

        with self.voiceover(text="Let's apply a filter to select employees whose Title is 'Engineer'. We use a Boolean indexing method to achieve this.") as tracker:
            self.add(subtitle_2)
            self.play(GrowFromCenter(console_2[0]), run_time=1)
            self.play(Write(console_2[1]), run_time=1)
            self.play(Write(console_2[2]), run_time=1)

        highlight_rectangles = highlight_rows([dataframe_rows[i] for i in [1, 2, 6]], range(6), YELLOW)
        self.play(*[Create(highlight) for highlight in highlight_rectangles])

        # Resultant DataFrame 1
        filtered_data = [
            ["Alice", "28", "Female", "Engineer", "85000", "5"],
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Frank", "29", "Male", "Engineer", "84000", "3"],
        ]

        filtered_rows = create_dataframe(headers, filtered_data, -1 * UP)
        filtered_index_column = create_index_column(["0", "1", "5"], filtered_rows[1:])

        self.play(TransformFromCopy(VGroup(*dataframe_rows[0]), VGroup(*filtered_rows[0])))  # Header row
        for original_row, new_row in zip([dataframe_rows[i] for i in [1, 2, 6]], filtered_rows[1:]):
            self.play(*[TransformFromCopy(orig_cell, new_cell) for orig_cell, new_cell in zip(original_row, new_row)])
        self.play(*[FadeIn(index) for index in filtered_index_column])
        self.wait(1)

        # -----Clean up Resultant DataFrame 1-----
        self.play(FadeOut(subtitle_2), FadeOut(console_2), *[FadeOut(index) for index in filtered_index_column], 
                  *[FadeOut(cell) for row in filtered_rows for cell in row], *[FadeOut(highlight) for highlight in highlight_rectangles])

        # -----Resultant DataFrame 2: Filter using ">"-----
        subtitle_3 = create_subtitle("Now, let's filter employees with a Salary greater than 90000.\nWe use the '>' operator for this filtering.")
        console_3 = create_console(13.9, 0.6, 0.4 * DOWN, DARK_GREY, 'employee_df[employee_df["Salary"] > 90000]')

        with self.voiceover(text="Now, let's filter employees with a Salary greater than 90000. We use the 'greater than' operator for this filtering.") as tracker:
            self.add(subtitle_3)
            self.play(GrowFromCenter(console_3[0]), run_time=1)
            self.play(Write(console_3[1]), run_time=1)
            self.play(Write(console_3[2]), run_time=1)

        highlight_rectangles_2 = highlight_rows([dataframe_rows[i] for i in [2,4]], range(6), YELLOW)
        self.play(*[Create(highlight) for highlight in highlight_rectangles_2])

        # Resultant DataFrame 2
        filtered_data_2 = [
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Diana", "40", "Female", "Manager", "105000", "10"]
        ]

        filtered_rows_2 = create_dataframe(headers, filtered_data_2, -1 * UP)
        filtered_index_column_2 = create_index_column(["1", "3"], filtered_rows_2[1:])

        self.play(TransformFromCopy(VGroup(*dataframe_rows[0]), VGroup(*filtered_rows_2[0])))  # Header row
        for original_row, new_row in zip([dataframe_rows[i] for i in [4]], filtered_rows_2[1:]):
            self.play(*[TransformFromCopy(orig_cell, new_cell) for orig_cell, new_cell in zip(original_row, new_row)])
        self.play(*[FadeIn(index) for index in filtered_index_column_2])
        self.wait(1)

        # -----Clean up Resultant DataFrame 2-----
        self.play(FadeOut(subtitle_3), FadeOut(console_3), *[FadeOut(index) for index in filtered_index_column_2], 
                *[FadeOut(cell) for row in filtered_rows_2 for cell in row], *[FadeOut(highlight) for highlight in highlight_rectangles_2])


        # -----Resultant DataFrame 3: Filter using "!="-----
        subtitle_4 = create_subtitle("Finally, let's filter employees whose Title is not 'Designer'.\nWe use the '!=' operator for this filtering.")
        console_4 = create_console(13.9, 0.6, 0.4 * DOWN, DARK_GREY, 'employee_df[employee_df["Title"] != "Designer"]')

        with self.voiceover(text="Finally, let's filter employees whose Title is not 'Designer'. We use the 'not equal to' operator for this filtering.") as tracker:
            self.add(subtitle_4)
            self.play(GrowFromCenter(console_4[0]), run_time=1)
            self.play(Write(console_4[1]), run_time=1)
            self.play(Write(console_4[2]), run_time=1)

        highlight_rectangles_3 = highlight_rows([dataframe_rows[i] for i in [1, 2, 4, 6]], range(6), YELLOW)
        self.play(*[Create(highlight) for highlight in highlight_rectangles_3])

        # Resultant DataFrame 3
        filtered_data_3 = [
            ["Alice", "28", "Female", "Engineer", "85000", "5"],
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Diana", "40", "Female", "Manager", "105000", "10"],
            ["Frank", "29", "Male", "Engineer", "84000", "3"],
        ]

        filtered_rows_3 = create_dataframe(headers, filtered_data_3, -1 * UP)
        filtered_index_column_3 = create_index_column(["0", "1", "3", "5"], filtered_rows_3[1:])

        self.play(TransformFromCopy(VGroup(*dataframe_rows[0]), VGroup(*filtered_rows_3[0])))  # Header row
        for original_row, new_row in zip([dataframe_rows[i] for i in [1, 2, 4, 6]], filtered_rows_3[1:]):
            self.play(*[TransformFromCopy(orig_cell, new_cell) for orig_cell, new_cell in zip(original_row, new_row)])
        self.play(*[FadeIn(index) for index in filtered_index_column_3])
        self.wait(1)

        # -----Clean up Resultant DataFrame 3-----
        self.play(FadeOut(subtitle_4), FadeOut(console_4), *[FadeOut(index) for index in filtered_index_column_3], 
                *[FadeOut(cell) for row in filtered_rows_3 for cell in row], *[FadeOut(highlight) for highlight in highlight_rectangles_3])
"""
