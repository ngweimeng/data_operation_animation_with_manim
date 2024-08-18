from openai import OpenAI
import os
import time

# Load API key from .env file
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def send_message_with_retries(prompt, model="gpt-4o-2024-08-06", max_retries=3):
    retry_wait = 60
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": (
                        "You are an expert educator and animator specializing in creating educational videos using Manim. "
                        "Your task is to generate Python code for Manim that explains a specific data operation step-by-step. "
                        "Follow the instructions provided in the user prompt carefully, focusing on generating a single resultant DataFrame after demonstrating the original DataFrame. "
                        "Ensure that the code is well-structured, includes detailed comments, and provides clear explanations with corresponding subtitles. "
                        "It is crucial that the resultant DataFrame accurately reflects the data operation applied to the original DataFrame. "
                        "Double-check that all rows meeting the criteria are included and that the resulting data matches the expected output exactly. "
                        "Voiceovers are not required."
                    )},
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(retry_wait)
            retry_wait *= 2  # Exponential backoff
    raise Exception("Max retries exceeded")
