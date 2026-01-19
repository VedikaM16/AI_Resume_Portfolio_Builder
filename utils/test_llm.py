from dotenv import load_dotenv
import os
print("STEP 1")

print("STEP 2")

load_dotenv()
print("STEP 3")

print("GEMINI KEY:", os.getenv("GEMINI_API_KEY"))
