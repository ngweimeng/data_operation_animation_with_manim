# 📊 Educational Animations for Data Operations

This project generates educational animations that visually explain various data operations in Python. The app leverages OpenAI's GPT-4 model to generate Python code for Manim, a powerful animation engine. These animations simplify complex data manipulation concepts, making them easier to understand.

## 🚀 Features

- **Generate Animations:** Automatically generate animations that explain different data operations using Manim.
- **Visualize Data Operations:** Includes topics like column selection, data filtering, grouping, aggregation, joining, and advanced reshaping.
- **Download Options:** Users can download the animations in both MP4 and GIF formats.
- **Interactive Interface:** The app is built with Streamlit, providing a user-friendly interface for selecting topics and generating videos.

## 📂 Directory Structure

```plaintext
├── generated_videos/          # Directory where generated videos are stored
├── final_video/               # Directory where final videos are stored for each tab
├── utils/                     # Utility scripts
│   ├── openai_helper.py       # Helper functions for OpenAI API
│   ├── file_operations.py     # Functions for file and directory operations
│   └── prompt_construction.py # Functions for constructing prompts
└── main.py                    # Main Streamlit app script
