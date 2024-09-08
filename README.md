# 🎥 Animated Data Operations

This project is an interactive web application designed to help beginners learn and understand data manipulation operations in Python using visually engaging animations. The app generates step-by-step animated videos for various data operations, making learning more intuitive and enjoyable.

## Features

- **Column Selection and Ordering**: Learn how to select and order rows and columns using different techniques.
- **Data Filtering**: Explore how to filter data based on conditions like equality, comparison, and handling null values.
- **Data Grouping and Aggregation**: Understand how to group data by columns and perform aggregation operations such as sum and mean.
- **Data Joining**: Learn how to join datasets using operations like inner, left, right, and outer joins.
- **Data Reshaping**: Master data reshaping techniques, including appending rows/columns, pivoting, and data melting.
- **Future Works**: View the app’s roadmap, which includes plans for automating video generation for other data manipulation languages such as R and SQL.

## How It Works

This app leverages OpenAI's GPT-4 model to generate Python code, which is then used to create educational animations with [Manim](https://www.manim.community/). These animations visually explain data operations, making it easier for users to grasp complex data concepts.

### Future Plans

- Automating the generation of videos for other data manipulation languages, such as R and SQL.
- Introducing multi-language support to generate videos and outputs in different programming languages.

## Getting Started

### Prerequisites

To run this project locally, you will need:

- Python 3.8 or higher
- [Streamlit](https://streamlit.io/)
- [Manim](https://www.manim.community/)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ngweimeng/data_operation_animation_with_manim
    ```

2. Navigate to the project directory:

    ```bash
    cd data_operation_animation_with_manim
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

### Usage

The app consists of several tabs, each demonstrating a different data operation:

1. **Column Selection and Ordering**: Learn how to organize and select data columns and rows.
2. **Data Filtering**: Explore techniques for filtering data based on conditions.
3. **Data Grouping and Aggregation**: Understand how to group and aggregate data for analysis.
4. **Data Joining**: Learn how to efficiently join multiple datasets.
5. **Data Reshaping**: Master techniques like pivoting and melting to reshape your data.
6. **Future Works**: Discover upcoming features and developments for the app.

Each tab provides educational videos with downloadable options in MP4 and GIF formats, allowing users to explore the operations at their own pace.

## Contributing

Contributions are welcome! If you would like to contribute, please check out the [GitHub project](https://github.com/ngweimeng/data_operation_animation_with_manim) to explore the codebase or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
