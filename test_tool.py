
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Create a dummy store just to get a name (or reuse one if I could, but creating is safer for a test)
# Actually, let's just try to generate content with a non-existent store name first to see if it passes the "tool_type" check.
# If it fails with "store not found", then the tool config is valid.
# If it fails with "tool_type" error, then the config is still invalid.

model_id = "gemini-2.0-flash"
tool_config = [
    {'file_search': {'file_search_store_names': ["projects/123/locations/us-central1/fileSearchStores/dummy"]}}
]

try:
    response = client.models.generate_content(
        model=model_id,
        contents="Hello",
        config=types.GenerateContentConfig(
            tools=tool_config
        )
    )
    print("Success (unexpected, should fail with store not found)")
except Exception as e:
    print(f"Error: {e}")
