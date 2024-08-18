def one_shot_prompt(operation):
    prompt = f"""
    You are an expert educator and animator specializing in using Manim to create educational videos. Your task is to create a detailed Manim script that explains the operation "{operation}" using Python.

    Please follow these specific steps to create the video:

    1. **Import Packages and Define Functions**:
       Reuse the provided example code to import the necessary Manim and Python packages, and define all required helper functions.

       Example:
       ```python
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
                   # Create the header row
                   header_row = create_row([f'<b>{{header}}</b>' for header in headers], pos_shift)
                   
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
                       table = create_cell(f'<span font_family="monospace">{{text}}</span>')
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
                           f'<span font_family="monospace"><b>{{index_value}}</b></span>',
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
       ```

    2. **Write Title**:
       Edit the title to clearly state the specific operation being demonstrated. Use the rest of the example code unchanged.

       Example:
       ```python
       title = MarkupText('{operation}', opacity=1).scale(0.5).shift(3.65 * UP)
       self.play(FadeIn(title))
       ```

    3. **Original DataFrame**:
       Reuse the provided example code to create and display the initial DataFrame with sample data. Ensure that the original DataFrame is consistent across all examples.

       Example:
       ```python
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

       self.add(subtitle_1)
       self.play(GrowFromCenter(console_1[0]), run_time=1)
       self.play(Write(console_1[1]), run_time=1)
       self.play(Write(console_1[2]), run_time=1)
       self.play(*[FadeIn(cell) for row in dataframe_rows for cell in row], *[FadeIn(index) for index in index_column_1])
       self.play(FadeOut(subtitle_1))
       ```

    4. **Create Resultant DataFrame**:
       - Apply the specified operation to the original DataFrame. The LLM must accurately identify the rows that meet the operation's criteria.
       - **Double-check the row indices to ensure correct highlighting and filtering.**
       - Explicitly state which indices correspond to each row in the DataFrame:
         - `1` corresponds to **Alice’s** row.
         - `2` corresponds to **Bob’s** row.
         - `3` corresponds to **Charlie’s** row.
         - `4` corresponds to **Diana’s** row.
         - `5` corresponds to **Eve’s** row.
         - `6` corresponds to **Frank’s** row.
       - Use the following method to highlight the correct rows:
         - For example, `highlight_rectangles = highlight_rows([dataframe_rows[i] for i in [1, 3, 6]], range(6), YELLOW)` would highlight Alice’s, Charlie’s, and Frank’s rows.
       - **Use conventional and simple pandas syntax**: The filtering code should be written in a way that is standard and commonly used by Python developers. Avoid overly complex or unnecessary conversions.
       - **Create the filtered DataFrame**: After highlighting, create the resultant DataFrame by including all rows that meet the filter criteria.
         - For example, if filtering by `Age < 30`, the resultant DataFrame should include:
           - Alice (Age 28)
           - Charlie (Age 25)
           - Frank (Age 29)
       - **Verify the filtered DataFrame**: 
         - Ensure that the resultant DataFrame exactly matches the expected output. 
         - **Double-check** that all rows that should be included are present and accurately reflect the operation applied.
         - **Explicitly compare** the resultant DataFrame against the original DataFrame to ensure no mistakes.
       - **Verification of Alignment**:
         - **Double-check** that the highlighted rows exactly match the rows in the resultant DataFrame. 
         - If a row is highlighted, it must appear in the resultant DataFrame, and vice versa.
       - **Checklist for Verification**:
         1. **Verify Index Mapping**: Confirm that the index numbers correspond to the correct rows.
         2. **Check Highlighting**: Ensure that only the correct rows are highlighted.
         3. **Check Filtered DataFrame**: Ensure that all rows meeting the filter criteria are included in the resultant DataFrame.
         4. **Match with Expected Result**: Compare the filtered rows with the expected outcome.
       - Provide subtitles that match the on-screen text. If the subtitle text exceeds 12 words, insert a `\n` character to split it onto a new line, ensuring that it remains readable on the screen.

       Example:
       ```python
       subtitle_2 = create_subtitle("Let's apply a filter to select employees whose Title is 'Engineer'.\nWe use a Boolean indexing method to achieve this.")
       console_2 = create_console(13.9, 0.6, 0.4 * DOWN, DARK_GREY, 'employee_df[employee_df["Title"] == "Engineer"]')

       self.add(subtitle_2)
       self.play(GrowFromCenter(console_2[0]), run_time=1)
       self.play(Write(console_2[1]), run_time=1)
       self.play(Write(console_2[2]), run_time=1)

       # Example 1: Filter by Title "Engineer"
       # Double-check: Alice (row 1), Bob (row 2), and Frank (row 6) should be highlighted for "Engineer" title
       highlight_rectangles = highlight_rows([dataframe_rows[i] for i in [1, 2, 6]], range(6), YELLOW)
       self.play(*[Create(highlight) for highlight in highlight_rectangles])

       filtered_data = [
           ["Alice", "28", "Female", "Engineer", "85000", "5"],
           ["Bob", "34", "Male", "Engineer", "95000", "6"],
           ["Frank", "29", "Male", "Engineer", "84000", "3"],
       ]

       filtered_rows = create_dataframe(headers, filtered_data, -1 * UP)
       filtered_index_column = create_index_column(["0", "1", "5"], filtered_rows[1:])

       self.play(TransformFromCopy(VGroup(*dataframe_rows[0]), VGroup(*filtered_rows[0])), run_time=1.2)  # Slow down for clarity
       for original_row, new_row in zip([dataframe_rows[i] for i in [1, 2, 6]], filtered_rows[1:]):
           self.play(*[TransformFromCopy(orig_cell, new_cell) for orig_cell, new_cell in zip(original_row, new_row)], run_time=1.2)
       self.play(*[FadeIn(index) for index in filtered_index_column], run_time=1.2)
       self.wait(1)

       # Example 2: Filter by Salary "> 90000"
       # For example, Bob (row 2) and Diana (row 4) should be highlighted if filtering by Salary > 90000
       highlight_rectangles = highlight_rows([dataframe_rows[i] for i in [2, 4]], range(6), YELLOW)
       self.play(*[Create(highlight) for highlight in highlight_rectangles])

       filtered_data_2 = [
           ["Bob", "34", "Male", "Engineer", "95000", "6"],
           ["Diana", "40", "Female", "Manager", "105000", "10"],
       ]

       filtered_rows_2 = create_dataframe(headers, filtered_data_2, -1 * UP)
       filtered_index_column_2 = create_index_column(["1", "3"], filtered_rows_2[1:])

       self.play(TransformFromCopy(VGroup(*dataframe_rows[0]), VGroup(*filtered_rows_2[0])), run_time=1.2)
       for original_row, new_row in zip([dataframe_rows[i] for i in [2, 4]], filtered_rows_2[1:]):
           self.play(*[TransformFromCopy(orig_cell, new_cell) for orig_cell, new_cell in zip(original_row, new_row)], run_time=1.2)
       self.play(*[FadeIn(index) for index in filtered_index_column_2], run_time=1.2)
       self.wait(1)
       ```

    Ensure that:
    - The generated Manim script is well-structured, with clear comments and explanations.
    - All strings are properly enclosed with matching quotes.
    - Code snippets within `MarkupText` are correctly escaped and formatted.
    - If the subtitle text exceeds 12 words, insert a `\n` character to split it onto a new line, ensuring that it remains readable on the screen.
    - The script is enclosed in triple backticks and formatted with the 'python' specifier, like this:
    ```python
    # Your Python code here
    ```

    Now, generate the script for the operation "{operation}" in Python.
    """
    return prompt



def construct_error_debugging_prompt(script_content, error_message):
    prompt = f"""
    You are an expert Manim script writer and debugger. The following Manim script failed with an error:

    Script:
    {script_content}

    Error Message:
    {error_message}

    Your task is to:
    1. Analyze the provided script and error message.
    2. Identify the cause of the error.
    3. Provide a corrected version of the script.
    4. Ensure the corrected script meets the initial requirements and does not introduce new errors.
    5. Ensure that only the corrected code is enclosed in triple backticks and formatted correctly with the 'python' specifier, like this:
    ```python
    # Your Python code here
    ```

    Please provide the corrected script in one complete block of code.
    """
    return prompt


