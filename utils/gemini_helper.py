import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def send_gemini_message_with_retries(prompt, model="gemini-1.5-pro", max_retries=3):
    retry_wait = 60
    for attempt in range(max_retries):
        try:
            response = genai.GenerativeModel(model).generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(retry_wait)
            retry_wait *= 2
    raise Exception("Max retries exceeded")
