import streamlit as st
import os
from datetime import datetime
from utils.openai_helper import send_message_with_retries
from utils.file_operations import ensure_directory_exists, render_manim_script, extract_code_blocks
from utils.prompt_construction import one_shot_prompt

def display_videos_for_tab(tab_name, operations):
    st.header(tab_name)
    for operation in operations:
        # Generate the file paths for both MP4 and GIF
        mp4_file_path = os.path.join(final_video_dir, f"{operation.lower().replace(' ', '_')}.mp4")
        gif_file_path = os.path.join(final_video_dir, f"{operation.lower().replace(' ', '_')}.gif")

        if os.path.exists(mp4_file_path):
            st.subheader(operation)
            st.video(mp4_file_path, loop=True, autoplay=True, muted=True)

            # Use st.columns to place buttons side by side
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
                # Check if the GIF version exists and provide a download button
                if os.path.exists(gif_file_path):
                    with open(gif_file_path, "rb") as gif_file:
                        st.download_button(
                            label="Download Video as GIF",
                            data=gif_file,
                            file_name=f"{operation}_Python.gif",
                            mime="image/gif"
                        )
            
            # Add a divider between each video block
            st.divider()
        else:
            st.warning(f"Video for {operation} is not available yet.")

# Directories for videos
final_video_dir = "final_video"
ensure_directory_exists(final_video_dir)

base_dir = "generated_videos"
ensure_directory_exists(base_dir)

# Streamlit app
st.title('📊 Educational Animations for Data Operations')

st.caption(
    "Explore and understand various data operations in Python with visually engaging animations. "
    "Generate videos that explain data manipulation concepts step by step."
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

tab2, tab3, tab4, tab5, tab6, tab1 = st.tabs([
    "Column Selection and Ordering", 
    "Data Filtering", 
    "Data Grouping and Aggregation", 
    "Data Joining", 
    "Advanced Data Reshaping", 
    "How it Works"
])

# Tab 1: Column Selection and Ordering
with tab2:
    operations = ["Select Columns by Name", "Select Columns by Index", "Select Rows by Name", "Select Rows by Index" ]
    display_videos_for_tab("Column Selection and Ordering", operations)

# Tab 2: Data Filtering
with tab3:
    operations = [
        "Filter with Equal",
        "Filter with Not Equal",
        "Filter with Greater Than",
        "Filter with Less Than",
        "Filter with AND",
        "Filter with OR",
        "Filter with NULL Values"
    ]
    display_videos_for_tab("Data Filtering", operations)

# Tab 3: Data Grouping and Aggregation
with tab4:
    operations = [
        "Sum Aggregation",
        "Mean Aggregation",
        "Group by",
        "Group by with Aggregation",
        "Group by Filtering"
    ]
    display_videos_for_tab("Data Grouping and Aggregation", operations)

# Tab 4: Data Joining
with tab5:
    operations = [
        "Inner Join", 
        "Left Join", 
        "Right Join", 
        "Full Outer Join",
        "Cross Join",
        "Self Join"
    ]
    display_videos_for_tab("Data Joining", operations)

# Tab 5: Advanced Data Reshaping
with tab6:
    operations = ["Pivot Table", "Data Melting"]
    display_videos_for_tab("Advanced Data Reshaping", operations)

# Tab 6: How it Works
with tab1:
    st.header("How this App Works")
    st.write(
        "This app leverages OpenAI's GPT-4 model to generate Python code, which is then used to create educational "
        "animations using Manim. These animations visually explain various data operations in Python, making complex "
        "concepts easier to grasp. "
    )
    st.warning("Note: The language model's generation is still a work in progress.", icon="⚠️")

    # Define the categories and their respective operations
    categories = {
        "Column Selection and Ordering": [
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
        "Data Grouping and Aggregation": [
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
        "Advanced Data Reshaping": [
            "Pivot Table", 
            "Data Melting"
        ]
    }

    # User inputs
    category = st.selectbox("Select a Topic", list(categories.keys()), key="category")
    operation = st.radio("Select a Data Operation", categories[category], key="operation")

    # Display the selected options
    st.markdown(f"**Category:** {category}")
    st.markdown(f"**Operation:** {operation}")

    # Generate and display the Manim script
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
                video_dir = os.path.join(base_dir, f"{operation}_Python_{timestamp}")
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
