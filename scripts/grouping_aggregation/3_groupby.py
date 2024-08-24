from manim import *

class GroupBy(Scene):
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
        title = MarkupText('GroupBy', color=GOLD).scale(0.7).shift(3.5 * UP)
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

        dataframe_rows = create_dataframe(headers, data, 2.3 * UP)
        index_column_1 = create_index_column(["0", "1", "2", "3", "4", "5"], dataframe_rows[1:])

        subtitle_1 = create_subtitle("Here is the initial DataFrame, 'df'.")
        console_1 = create_console(13.9, 0.6, 2.9 * UP, DARK_GREY, 'df')

        self.add(subtitle_1)
        self.play(FadeIn(console_1), *[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
        self.wait(1)
        self.play(FadeOut(subtitle_1))

        # -----GroupBy Without Aggregation-----
        subtitle_2 = create_subtitle("Next, we group the data by 'Title'.")
        console_2 = create_console(13.9, 0.6, 0.6 * DOWN, DARK_GREY, 'df.groupby("Title")')

        self.add(subtitle_2)
        self.play(FadeIn(console_2))
        self.wait(1)

        # Highlight the 'Title' column based on grouping
        highlight_rectangles_engineer = highlight_rows([dataframe_rows[i] for i in [1, 2, 6]], range(6), YELLOW)
        highlight_rectangles_designer = highlight_rows([dataframe_rows[i] for i in [3, 5]], range(6), BLUE)
        highlight_rectangles_manager = highlight_rows([dataframe_rows[i] for i in [4]], range(6), RED)
        self.play(*[Create(highlight) for highlight in highlight_rectangles_engineer])
        self.play(*[Create(highlight) for highlight in highlight_rectangles_designer])
        self.play(*[Create(highlight) for highlight in highlight_rectangles_manager])

        grouped_data = [
            ["Designer", "Charlie", "25", "Male", "55000", "2"],
            ["Designer", "Eve", "30", "Female", "90000", "4"],
            ["Engineer", "Alice", "28", "Female", "85000", "5"],
            ["Engineer", "Bob", "34", "Male", "95000", "6"],
            ["Engineer", "Frank", "29", "Male", "84000", "3"],
            ["Manager", "Diana", "40", "Female", "105000", "10"]
        ]
        grouped_headers = ["Title", "Name", "Age", "Gender", "Salary", "Experience"]
        
        grouped_dataframe_rows = create_dataframe(grouped_headers, grouped_data, -1.2 * UP)

        highlight_rectangles_engineer_res = highlight_rows([grouped_dataframe_rows[i] for i in [3, 4, 5]], range(6), YELLOW)
        highlight_rectangles_designer_res = highlight_rows([grouped_dataframe_rows[i] for i in [1, 2]], range(6), BLUE)
        highlight_rectangles_manager_res = highlight_rows([grouped_dataframe_rows[i] for i in [6]], range(6), RED)

        self.play(FadeOut(subtitle_2))
        
        # Fade in header row
        self.play(FadeIn(VGroup(*grouped_dataframe_rows[0]))) 

        # Combine transformations for designer rows and highlights
        designer_combined_transform = [
            TransformFromCopy(orig_cell, new_cell)
            for original_row, new_row in zip([dataframe_rows[i] for i in [3, 5]], grouped_dataframe_rows[1:3])
            for orig_cell, new_cell in zip(original_row, new_row)
        ] + [
            TransformFromCopy(orig_highlight, new_highlight)
            for orig_highlight, new_highlight in zip(highlight_rectangles_designer, highlight_rectangles_designer_res)
        ]
        self.play(AnimationGroup(*designer_combined_transform, lag_ratio=0), run_time=1.75)

        # Combine transformations for engineer rows and highlights
        engineer_combined_transform = [
            TransformFromCopy(orig_cell, new_cell)
            for original_row, new_row in zip([dataframe_rows[i] for i in [1, 2, 6]], grouped_dataframe_rows[3:6])
            for orig_cell, new_cell in zip(original_row, new_row)
        ] + [
            TransformFromCopy(orig_highlight, new_highlight)
            for orig_highlight, new_highlight in zip(highlight_rectangles_engineer, highlight_rectangles_engineer_res)
        ]
        self.play(AnimationGroup(*engineer_combined_transform, lag_ratio=0), run_time=1.75)

        # Combine transformations for manager row and highlight
        manager_combined_transform = [
            TransformFromCopy(orig_cell, new_cell)
            for orig_cell, new_cell in zip(dataframe_rows[4], grouped_dataframe_rows[6])
        ] + [
            TransformFromCopy(orig_highlight, new_highlight)
            for orig_highlight, new_highlight in zip(highlight_rectangles_manager, highlight_rectangles_manager_res)
        ]
        self.play(AnimationGroup(*manager_combined_transform, lag_ratio=0), run_time=1.75)

        self.wait(1)