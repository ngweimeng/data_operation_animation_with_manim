import os
import subprocess
import re
import uuid
from utils.openai_helper import send_message_with_retries

def ensure_directory_exists(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except FileExistsError:
        pass

def render_manim_script(script_content, output_dir, max_retries=3):
    ensure_directory_exists(output_dir)
    
    script_path = os.path.join(output_dir, f"{uuid.uuid4().hex[:8]}.py")
    with open(script_path, "w", encoding="utf-8") as file:
        file.write(script_content)
    
    for attempt in range(max_retries):
        result = subprocess.run(
            ["manim", "-pql", script_path, "--media_dir", output_dir, "--disable_caching"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            return result.stdout, result.stderr, None  # No error

        # If there is an error, use the LLM to debug
        error_message = result.stderr
        prompt = f"The following Manim script failed with an error:\n\n{script_content}\n\nError:\n{error_message}\n\nPlease debug and provide a corrected version of the script."
        response_text = send_message_with_retries(prompt)
        corrected_code_blocks = extract_code_blocks(response_text)
        if corrected_code_blocks:
            script_content = corrected_code_blocks[0].strip()
            with open(script_path, "w", encoding="utf-8") as file:
                file.write(script_content)
        else:
            break

    return result.stdout, result.stderr, error_message


def extract_code_blocks(text):
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches
