from manim import *

class Stack(Scene):
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

        def create_row(texts, y_shift, fill_color=None, is_header=False, is_bottom_dataframe=False):
            row = []
            previous_table = None
            for text in texts:
                # For the blank header cell in the bottom dataframe, pass is_blank_header=True
                if is_bottom_dataframe and text == " ":
                    table = create_cell(text, fill_color=None, is_blank_header=True)
                else:
                    table = create_cell(text, fill_color=fill_color, is_header=is_header)

                if previous_table is None:
                    table.shift(y_shift + 4.5 * LEFT)
                else:
                    table.next_to(previous_table, RIGHT, buff=0) 
                row.append(table)
                previous_table = table
            return row

        def create_cell(text, fill_color=None, is_header=False, is_blank_header=False):
            cell = Rectangle(width=3, height=0.6)

            # For blank header in the bottom dataframe, no stroke and no fill
            if is_blank_header:
                cell.set_stroke(opacity=0)  # No stroke
                cell.set_fill(opacity=0)    # No fill
            # Apply grey fill to the "Score" header cell
            elif text == "Score":
                cell.set_stroke(color=GREY, opacity=1)  # Apply stroke for the "Score" header
                cell.set_fill(GREY_D, opacity=1)  # Fill the "Score" header with grey
            # For headers in the top dataframe, set stroke even for Math and Science
            elif is_header:
                cell.set_stroke(color=GREY, opacity=1)  # Stroke for headers
                if fill_color:
                    cell.set_fill(fill_color, opacity=1)
            # Default condition for other cells (no stroke for Math and Science in the bottom dataframe)
            elif "Math" in text or "Science" in text:
                cell.set_stroke(opacity=0)  # No stroke for Math and Science in bottom dataframe
            else:
                cell.set_stroke(color=GREY, opacity=1)  # Default stroke for other cells

            cell.scale(0.6)

            # Set the text with monospaced font (same as the index)
            text = MarkupText(f'<span font_family="monospace">{text}</span>').scale(0.4)
            
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
        title = MarkupText('Stack', color=GOLD).scale(0.7).shift(3.5 * UP)
        self.play(FadeIn(title))

        # -----Original DataFrame-----
        headers = ["Name", "Math", "Science"]
        data = [
            ["Alice", "85", "90"],
            ["Bob", "75", "85"],
            ["Charlie", "95", "89"]
        ]

        # Create the header row with a stroke for all headers, including "Math" and "Science"
        header_row_top = create_row([f'<b>{header}</b>' for header in headers], 2.3 * UP + 2.5 * RIGHT, fill_color=GREY_D, is_header=True)

        # Create the data rows (without the header)
        dataframe_rows = [header_row_top] + [create_row(row_data, 2.3 * UP + 2.5 * RIGHT - (i + 1) * 0.35 * UP) for i, row_data in enumerate(data)]
        index_column_1 = create_index_column(["0", "1", "2"], dataframe_rows[1:])

        subtitle_1 = create_subtitle("Here is the initial DataFrame, 'df'.")
        console_1 = create_console(13.9, 0.6, 2.9 * UP, DARK_GREY, 'df')

        self.add(subtitle_1)
        self.play(FadeIn(console_1), *[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
        self.wait(1)
        self.play(FadeOut(subtitle_1))

        # -----Explanation of df.set_index("Name").stack()-----
        subtitle_2 = create_subtitle("We set 'Name' as the index, stack the 'Math' and 'Science' columns, and rename the result as 'Score'.")
        console_2 = create_console(13.9, 0.6, 0 * DOWN, DARK_GREY, 'df.set_index("Name").stack().rename("Score")')

        self.add(subtitle_2)
        self.play(FadeIn(console_2))
        self.wait(1)

        # -----Stacked DataFrame-----
        stacked_data = [
            ["Math", "85"], ["Science", "90"],
            ["Math", "75"], ["Science", "85"],
            ["Math", "95"], ["Science", "89"]
        ]

        # Create the header row for the bottom DataFrame
        # Ensuring the blank header cell (" ") has no stroke and no fill
        header_row_bottom = create_row([" ", "Score"], -0.6 * UP + 2.5 * RIGHT, fill_color=GREY_D, is_bottom_dataframe=True)

        # Create the stacked data rows, with no stroke for "Math" and "Science"
        stacked_rows = [header_row_bottom] + [create_row(row_data, -0.6 * UP + 2.5 * RIGHT - (i + 1) * 0.35 * UP) for i, row_data in enumerate(stacked_data)]
        index_column_2 = create_index_column(["Name", "Alice", " ", "Bob", " ", "Charlie", " "], stacked_rows[0:])

        highlight_rectangles_alice = highlight_rows([dataframe_rows[i] for i in [1]], range(1, 3), YELLOW)
        highlight_rectangles_bob = highlight_rows([dataframe_rows[i] for i in [2]], range(1, 3), BLUE)
        highlight_rectangles_charlie = highlight_rows([dataframe_rows[i] for i in [3]], range(1, 3), RED)
        self.play(*[Create(highlight) for highlight in highlight_rectangles_alice])
        self.play(*[Create(highlight) for highlight in highlight_rectangles_bob])
        self.play(*[Create(highlight) for highlight in highlight_rectangles_charlie])

        highlight_rectangles_alice_res = highlight_rows([stacked_rows[i] for i in [1, 2]], range(1, 2), YELLOW)
        highlight_rectangles_bob_res = highlight_rows([stacked_rows[i] for i in [3, 4]], range(1, 2), BLUE)
        highlight_rectangles_charlie_res = highlight_rows([stacked_rows[i] for i in [5, 6]], range(1, 2), RED)

        self.play(FadeIn(VGroup(*stacked_rows[0])))

        alice_transform = [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in stacked_rows[1:3] for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in highlight_rectangles_alice_res for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in index_column_2[0:2] for cell in row]))
        ]
        self.play(AnimationGroup(*alice_transform, lag_ratio=0), run_time=1.75)

        bob_transform = [
            TransformFromCopy(Group(*highlight_rectangles_bob), Group(*[cell for row in stacked_rows[3:5] for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_bob), Group(*[cell for row in highlight_rectangles_bob_res for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in index_column_2[2:4] for cell in row]))
        ]
        self.play(AnimationGroup(*bob_transform, lag_ratio=0), run_time=1.75)

        charlie_transform = [
            TransformFromCopy(Group(*highlight_rectangles_charlie), Group(*[cell for row in stacked_rows[5:7] for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_charlie), Group(*[cell for row in highlight_rectangles_charlie_res for cell in row]))
        ] + [
            TransformFromCopy(Group(*highlight_rectangles_alice), Group(*[cell for row in index_column_2[4:6] for cell in row]))
        ]
        self.play(AnimationGroup(*charlie_transform, lag_ratio=0), run_time=1.75)
        
        self.wait(2)