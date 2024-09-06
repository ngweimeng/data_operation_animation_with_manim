from manim import *

class Join(Scene):
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
        
        def highlight_columns(rows, columns, color):
            highlights = []
            for row in rows:
                for i in columns:
                    highlight = create_highlight(3, 0.6, color).move_to(row[i].get_center())
                    highlights.append(highlight)
            return highlights
        
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
        title = MarkupText('Right Join', color=GOLD).scale(0.7).shift(3.5 * UP)
        self.play(FadeIn(title))

        # -----Pre-Joined DataFrames-----
        headers1 = ["Name", "Age", "Gender"]
        data1 = [
            ["Alice", "28", "Female"],
            ["Bob", "34", "Male"],
            ["Charlie", "25", "Male"],
            ["Diana", "40", "Female"],
            ["Eve", "30", "Female"],
        ]

        headers2 = ["Name", "Title", "Salary"]
        data2 = [
            ["Alice", "Engineer", "85000"],
            ["Bob", "Engineer", "95000"],
            ["Charlie", "Designer", "55000"],
            ["Diana", "Manager", "105000"],
            ["Frank", "Designer", "90000"],
        ]

        dataframe_rows_1 = create_dataframe(headers1, data1, 2.3 * UP)
        for row in dataframe_rows_1:
            for cell in row:
                cell.shift(0.5 * LEFT)
        index_column_1 = create_index_column(["0", "1", "2", "3", "4"], dataframe_rows_1[1:])

        dataframe_rows_2 = create_dataframe(headers2, data2, 2.3 * UP)
        for row in dataframe_rows_2:
            for cell in row:
                cell.shift(6.5 * RIGHT)
        index_column_2 = create_index_column(["0", "1", "2", "3", "4"], dataframe_rows_2[1:])

        subtitle_1 = create_subtitle("Here are two DataFrames, 'df1' and 'df2'.")
        console_1 = create_console(6, 0.6, 2.9 * UP + 3.5 * LEFT, DARK_GREY, 'df1')
        console_2 = create_console(6, 0.6, 2.9 * UP + 3.5 * RIGHT, DARK_GREY, 'df2')

        self.add(subtitle_1)
        self.play(
            FadeIn(console_1), 
            *[FadeIn(cell) for row in dataframe_rows_1 for cell in row],
            *[FadeIn(index) for index in index_column_1],
            FadeIn(console_2), 
            *[FadeIn(cell) for row in dataframe_rows_2 for cell in row],
            *[FadeIn(index) for index in index_column_2]
        )
        self.wait(1)
        self.play(FadeOut(subtitle_1))

         # -----Joining on "Name"-----
        subtitle_2 = create_subtitle("Next, we join the two DataFrames on the 'Name' column using a Right Join.")
        console_2 = create_console(13.9, 0.6, 0.6 * DOWN, DARK_GREY, 'pd.merge(df1, df2, on="Name", how="right")')

        self.add(subtitle_2)
        self.play(FadeIn(console_2))
        self.wait(1)

        # Highlight "Name" column in both DataFrames
        highlight_columns_name_1 = highlight_columns(dataframe_rows_1, [0], YELLOW)  
        highlight_columns_name_2 = highlight_columns(dataframe_rows_2, [0], YELLOW)  
        self.play(*[Create(highlight) for highlight in highlight_columns_name_1 + highlight_columns_name_2])

        # -----Resultant DataFrame-----
        headers3 = ["Name", "Age", "Gender", "Title", "Salary"]
        data3 = [
            ["Alice", "28", "Female", "Engineer", "85000"],
            ["Bob", "34", "Male", "Engineer", "95000"],
            ["Charlie", "25", "Male", "Designer", "55000"],
            ["Diana", "40", "Female", "Manager", "105000"],
            ["Frank", " ", " ", "Designer", "90000"],
        ]

        resultant_dataframe_rows = create_dataframe(headers3, data3, -1.2 * UP)
        resultant_index_column = create_index_column(["0", "1", "2", "3", "4"], resultant_dataframe_rows[1:])

        self.play(FadeIn(VGroup(*resultant_dataframe_rows[0])))
        # Loop over each row to perform the transformations
        for row_index in range(1, 5):

            # Collect transformations from df_employee
            employee_transforms = [
                TransformFromCopy(orig_cell, new_cell)
                for orig_cell, new_cell in zip(dataframe_rows_1[row_index], resultant_dataframe_rows[row_index])
            ]
            
            # Collect transformations from df_salary
            salary_transforms = [
                TransformFromCopy(orig_cell, new_cell)
                for orig_cell, new_cell in zip(dataframe_rows_2[row_index][1:3], resultant_dataframe_rows[row_index][3:5])
            ]
            
            # Play the transformations for both DataFrames together for each row
            self.play(*(employee_transforms + salary_transforms), run_time=1.75)
        
        # Play the transformations for the last row separately
        row_index = 5 
        animations = [
            TransformFromCopy(dataframe_rows_2[row_index][i], resultant_dataframe_rows[row_index][i + 2])
            for i in range(1, 3)  
        ] + [
            FadeIn(resultant_dataframe_rows[row_index][i])
            for i in range(1, 3)  # Loop over the 4th and 5th columns (Title, Salary)
        ] + [
            TransformFromCopy(dataframe_rows_2[row_index][0], resultant_dataframe_rows[row_index][0])
        ]

        self.play(*animations, run_time=1.75)

        self.play(*[FadeIn(index) for index in resultant_index_column])
        self.wait(1)
        self.play(FadeOut(subtitle_2))

        # Right Join Explanation
        subtitle_3 = create_subtitle("A right join includes all rows from the right table, but only the matching rows from the left table.")
        highlight_rectangles = highlight_rows([resultant_dataframe_rows[i] for i in [5]], range(5), BLUE)
        self.play(*[Create(highlight) for highlight in highlight_rectangles])
        self.add(subtitle_3)
        self.wait(1)