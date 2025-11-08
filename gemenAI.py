from google import genai
import os
import google.genai.errors
import time
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


api_key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)
# -----------------------------
# Get Solution from the model
# -----------------------------
# We are using retries cause sometime google API can fail so at least we dont give error with first try
def getSolution(prompt, retires=5):
    for attempt in range(retires):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            generated_text = response.text

            return generated_text
        except google.genai.errors.ServerError as e:
            if "503" in str(e):
                wait = 2 ** attempt  # exponential backoff
                print(f"[WARN] Gemini overloaded, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


    print("[ERROR] Gemini API still unavailable after retries.")
    return None


