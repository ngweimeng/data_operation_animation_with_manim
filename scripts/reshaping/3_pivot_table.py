from manim import *

class PivotTable(Scene):
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
        title = MarkupText('Pivot Table', color=GOLD).scale(0.7).shift(3.5 * UP)
        self.play(FadeIn(title))

        # -----Original DataFrame-----
        headers = ["Name", "Age", "Gender", "Title", "Salary", "Experience"]
        data = [
            ["Alice", "28", "Female", "Engineer", "85000", "5"],
            ["Bob", "34", "Male", "Engineer", "95000", "6"],
            ["Charlie", "25", "Male", "Designer", "55000", "2"],
            ["Diana", "40", "Female", "Manager", "105000", "10"],
            ["Eve", "30", "Female", "Designer", "90000", "4"],
            ["Frank", "29", "Male", "Engineer", "84000", "3"]
        ]

        dataframe_rows = create_dataframe(headers, data, 2.3 * UP)
        index_column_1 = create_index_column([str(i) for i in range(6)], dataframe_rows[1:])

        subtitle_1 = create_subtitle("Here is the initial DataFrame, 'df'.")
        console_1 = create_console(13.9, 0.6, 2.9 * UP, DARK_GREY, 'df')

        self.add(subtitle_1)
        self.play(FadeIn(console_1), *[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
        self.wait(1)
        self.play(FadeOut(subtitle_1))

        # -----Pivot Table with Gender as Column-----
        subtitle_2 = create_subtitle("We will now use a Pivot Table to summarize the Salary data by Title and Gender.")
        self.add(subtitle_2)
        self.play(FadeIn(subtitle_2))
        console_2 = create_console(13.9, 0.6, 0.6 * DOWN, DARK_GREY, 'df.pivot_table(values="Salary", index="Title", columns="Gender", aggfunc="mean")')
        self.play(FadeIn(console_2))
        self.wait(2)
        self.play(FadeOut(subtitle_2))

        subtitle_4 = create_subtitle("This means that for each unique Title, we'll see the average Salary split by Gender.")
        self.play(FadeIn(subtitle_4))
        self.wait(1)

        # Highlight the Title and Gender columns
        highlight_title_column = highlight_rows(dataframe_rows[1:], [3], YELLOW)
        highlight_gender_column = highlight_rows(dataframe_rows[1:], [2], BLUE)
        self.play(*[Create(highlight) for highlight in highlight_title_column + highlight_gender_column])

        pivot_headers = ["Title", "Female", "Male"]
        pivot_data = [
            ["Designer", "90000", "55000"],
            ["Engineer", "85000", "89500"],
            ["Manager", "105000", "NaN"]
        ]

        pivot_dataframe_rows = create_dataframe(pivot_headers, pivot_data, -1.2 * UP)
        filtered_index_column = create_index_column(["0", "1", "2"], pivot_dataframe_rows[1:])

        self.play(TransformFromCopy(VGroup(*highlight_gender_column),VGroup(*pivot_dataframe_rows[0])),run_time=1.75)
        self.play(TransformFromCopy(VGroup(*highlight_title_column), VGroup(*[row[0] for row in pivot_dataframe_rows[1:]])),run_time=1.75)

        self.play(FadeOut(subtitle_4))

        # Display pivot table result
        highlight_salary_column = highlight_rows(dataframe_rows[1:], [4], RED)
        subtitle_5 = create_subtitle("The resulting Pivot Table will display the average Salary for each Title and Gender.")
        self.play(FadeIn(subtitle_5))
        self.play(*[Create(highlight) for highlight in highlight_salary_column])
        self.wait(1)
        # Group the highlights into pairs (2 per pivot row)
        grouped_highlights = [
            VGroup(highlight_salary_column[i], highlight_salary_column[i + 1])
            for i in range(0, len(highlight_salary_column), 2)
        ]

        # Create transformations from each pair of highlights to the corresponding pivot row
        transformations = [
            TransformFromCopy(group, VGroup(*pivot_row[1:]))
            for group, pivot_row in zip(grouped_highlights, pivot_dataframe_rows[1:])
        ]

        # Play all transformations at once
        self.play(*transformations, run_time=1.75)
                
        self.wait(1)
        self.play(FadeOut(subtitle_5))

        self.play(*[FadeIn(index) for index in filtered_index_column])

        subtitle_6 = create_subtitle("For example, the average salary for Designers is $90,000 for Females and $55,000 for Males.")
        self.play(FadeIn(subtitle_6))
        self.wait(2)