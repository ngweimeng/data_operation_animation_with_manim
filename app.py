import streamlit as st
import os
from datetime import datetime
from utils.openai_helper import send_message_with_retries
from utils.file_operations import ensure_directory_exists, render_manim_script, extract_code_blocks
from utils.prompt_construction import one_shot_prompt

def display_video(operation):
    # Generate the file paths for both MP4 and GIF
    mp4_file_path = os.path.join(final_video_dir, f"{operation.replace(' ', '_')}.mp4")
    gif_file_path = os.path.join(final_video_dir, f"{operation.replace(' ', '_')}.gif")

    if os.path.exists(mp4_file_path):
        # Adjusted to fit within the column
        st.video(mp4_file_path, start_time=0)
        
        # Place download buttons side by side
        col1, col2 = st.columns(2)

        with col1:
            # Download MP4 button
            with open(mp4_file_path, "rb") as mp4_file:
                st.download_button(
                    label="Download Video as MP4",
                    data=mp4_file,
                    file_name=f"{operation}_Python.mp4",
                    mime="video/mp4"
                )

        with col2:
            # Download GIF button
            if os.path.exists(gif_file_path):
                with open(gif_file_path, "rb") as gif_file:
                    st.download_button(
                        label="Download Video as GIF",
                        data=gif_file,
                        file_name=f"{operation}_Python.gif",
                        mime="image/gif"
                    )

    else:
        st.warning(f"Video for {operation} is not available yet.")

# Directories for videos
final_video_dir = "videos"
ensure_directory_exists(final_video_dir)

base_dir = "generated_videos"
ensure_directory_exists(base_dir)

# Streamlit app
st.set_page_config(
    page_title="Animated Data Operations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('🎥 Animated Data Operations')
st.markdown(
    "Learn essential data manipulation techniques in Python through step-by-step animated videos, designed to make learning more intuitive and engaging."
)

with st.expander("How to Use This Webpage❓"):
    st.markdown(
        """
        1. **Select a Topic:** Use the tabs below to choose a topic you're interested in, such as "📊 Column Selection" or "🔍 Data Filtering".

        2. **Choose an Operation:** Within each tab, use the dropdown menu to select a specific data operation you want to learn about.

        3. **View the Video:** The corresponding animated video for the selected operation will be displayed next to the dropdown menu.

        4. **Download the Video:** You can download the video in MP4 or GIF format using the download buttons provided under the video.
        """
    )

# "About the App" section
with st.sidebar:
    st.header("About the Project")
    st.write(
        """
        This project is designed to help beginners understand data manipulation operations in Python using visually engaging animations. 
        Each animation explains common data tasks, making it easier to grasp complex concepts.
        
        **Future Plans:**
        - Utilize a LLM to automate video generation in other programming languages such as R and SQL.
        - Introducing multi-language support, allowing users to generate voiceover and subtitles in their chosen language.
        
        **Contribute or Explore More:**
        Check out the [GitHub project](https://github.com/ngweimeng/data_operation_animation_with_manim) for more information. 
        Feel free to contribute or explore the codebase if you're interested!

        **Feedback:**
        I am always looking to improve the project. If you have any feedback or suggestions, please fill out this
        https://forms.gle/V4wcQtEtqEbTHUma7
        """
    )

# CSS adjustments for tabs and overall layout
st.markdown(
    """
    <style>
    /* Inactive tabs */
    button[data-baseweb="tab"] {
        background-color: #d6d3dd;
        color: #333333;
        border: 1px solid #b3b0bd;
        padding: 8px 16px; /* Reduced padding */
        margin-right: 2px;  /* Reduced margin */
        border-radius: 5px;
    }
    /* Active tab */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #6a5acd;
        color: white;
        border-bottom: 2px solid #483d8b;
        padding: 8px 16px;
        margin-right: 2px;
        border-radius: 5px;
    }
    /* Hover effect */
    button[data-baseweb="tab"]:hover {
        background-color: #cbc8d3;
        cursor: pointer;
    }
    /* Tab label styling */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        font-weight: 500;
        font-family: 'Courier New', Courier, monospace !important;
        margin: 0;
        line-height: 1.2; /* Adjusted line height */
    }
    /* Reduce padding around main content */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    /* Allow tabs to wrap onto multiple lines */
    .stTabs [role="tablist"] {
    flex-wrap: wrap;
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""
if 'response_text' not in st.session_state:
    st.session_state.response_text = ""
if 'script_content' not in st.session_state:
    st.session_state.script_content = ""
if 'video_file_path' not in st.session_state:
    st.session_state.video_file_path = ""
if 'video_generated' not in st.session_state:
    st.session_state.video_generated = False

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Column Selection",
    "🔍 Data Filtering",
    "📈 Grouping & Aggregation",
    "🔗 Data Joining",
    "🔄 Data Reshaping",
    "ℹ️ Future Works"
])

# Tab 1: Column Selection and Ordering
with tab1:
    st.markdown("Learn how to organize and select columns and rows effectively.")
    operations = ["Select Columns by Name", "Select Columns by Index", "Select Rows by Name", "Select Rows by Index"]
    # Use columns to place selectbox and video side by side
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_operation = st.selectbox("Select an Operation", operations, key="tab1_operation")
    with col2:
        display_video(selected_operation)

# Tab 2: Data Filtering
with tab2:
    st.markdown("Explore techniques to filter your data based on various conditions.")
    operations = [
        "Filter with Equal",
        "Filter with Not Equal",
        "Filter with Greater Than",
        "Filter with Less Than",
        "Filter with AND",
        "Filter with OR",
        "Filter with NULL Values"
    ]
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_operation = st.selectbox("Select an Operation", operations, key="tab2_operation")
    with col2:
        display_video(selected_operation)

# Tab 3: Data Grouping and Aggregation
with tab3:
    st.markdown("Learn how to group and aggregate your data for deeper analysis.")
    operations = [
        "Sum Aggregation",
        "Mean Aggregation",
        "Group by",
        "Group by with Aggregation",
        "Group by with Filtering"
    ]
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_operation = st.selectbox("Select an Operation", operations, key="tab3_operation")
    with col2:
        display_video(selected_operation)

# Tab 4: Data Joining
with tab4:
    st.markdown("Understand how to join different datasets together efficiently.")
    operations = [
        "Inner Join",
        "Left Join",
        "Right Join",
        "Outer Join"
    ]
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_operation = st.selectbox("Select an Operation", operations, key="tab4_operation")
    with col2:
        display_video(selected_operation)

# Tab 5: Data Reshaping
with tab5:
    st.markdown("Master reshaping data using techniques like pivoting and melting.")
    operations = [
        "Concat Horizontally",
        "Concat Vertically",
        "Pivot Table",
        "Data Melting",
        "Stack"
    ]
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_operation = st.selectbox("Select an Operation", operations, key="tab5_operation")
    with col2:
        display_video(selected_operation)

# Tab 6: Future Works
with tab6:
    st.header("Future Works")
    st.write(
        "This app leverages OpenAI's GPT-4 model to generate Python code, which is then used to create educational "
        "animations using Manim. These animations visually explain various data operations in Python, making complex "
        "concepts easier to grasp. "
    )
    st.warning("Note: The language model's generation is still a work in progress.", icon="⚠️")

    # Define the categories and their respective operations
    categories = {
        "Column Selection": [
            "Select Columns by Name",
            "Select Columns by Index",
        ],
        "Data Filtering": [
            "Filter with Comparison Operator: Equal (==)",
            "Filter with Comparison Operator: Not Equal (!=)",
            "Filter with Comparison Operator: Greater Than (>)",
            "Filter with Comparison Operator: Less Than (<)",
            "Filter with AND",
            "Filter with OR",
            "Filter with NULL Values"
        ],
        "Grouping and Aggregation": [
            "Sum Aggregation",
            "Mean Aggregation",
            "Group by Single Column",
            "Group by with Aggregation",
            "HAVING Clause Filtering"
        ],
        "Data Joining": [
            "Inner Join",
            "Left Join",
            "Right Join",
            "Full Outer Join",
            "Cross Join",
            "Self Join"
        ],
        "Data Reshaping": [
            "Concat Horizontally",
            "Concat Vertically",
            "Pivot Table",
            "Data Melting",
            "Stack"
        ]
    }

    category = st.selectbox("Select a Topic", list(categories.keys()), key="category")
    operation = st.radio("Select a Data Operation", categories[category], key="operation")

    st.markdown(f"**Category:** {category}")
    st.markdown(f"**Operation:** {operation}")

    if st.button('Generate Video'):
        st.session_state.prompt = one_shot_prompt(operation)

        try:
            with st.spinner('Generating Manim script...'):
                st.session_state.response_text = send_message_with_retries(st.session_state.prompt)
            with st.expander("See Generated Code"):
                st.code(st.session_state.response_text, language='python')

            # Extract Manim script
            st.session_state.script_content = extract_code_blocks(st.session_state.response_text)[0].strip()
            with st.expander("See Manim Script"):
                st.code(st.session_state.script_content, language='python')

            # Render the Manim Script
            max_debug_attempts = 6
            debug_attempts = 0
            success = False

            while debug_attempts < max_debug_attempts and not success:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_dir = os.path.join("generated_videos", f"{operation}_Python_{timestamp}")
                ensure_directory_exists(video_dir)

                with st.spinner('Rendering video...'):
                    stdout, stderr, error_message = render_manim_script(st.session_state.script_content, video_dir)
                    with st.expander("See Render Logs"):
                        st.write(stdout)
                        st.write(stderr)

                    if error_message:
                        st.error(f"An error occurred while rendering the video: {error_message}")
                        debug_attempts += 1
                    else:
                        success = True
                        # Find the video file in the nested directories
                        st.session_state.video_file_path = None
                        for root, dirs, files in os.walk(video_dir):
                            video_files = [f for f in files if f.endswith('.mp4')]
                            if video_files:
                                st.session_state.video_file_path = os.path.join(root, video_files[0])
                                break

                        st.session_state.video_generated = True

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.video_generated = False

    # Display previous state if available and video is generated successfully
    if st.session_state.video_generated:
        if st.session_state.response_text:
            with st.expander("See Generated Code"):
                st.code(st.session_state.response_text, language='python')

        if st.session_state.script_content:
            with st.expander("See Manim Script"):
                st.code(st.session_state.script_content, language='python')

        if st.session_state.video_file_path:
            st.text("See the rendered video below:")
            st.video(st.session_state.video_file_path)

            with open(st.session_state.video_file_path, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=f"{operation}_Python.mp4",
                    mime="video/mp4"
                )
