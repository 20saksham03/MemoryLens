import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


def analyze_screenshot(image_bytes: bytes, mime_type: str) -> dict:
    prompt = """
You are the vision intelligence engine for MemoryLens.

Analyze the provided screenshot and extract structured information.

Determine:

1. title
2. summary
3. category
4. intent
5. keywords
6. entities
7. date
8. price
9. location

Category should be one of:
Shopping, Travel, Recipes, Bills, Finance, Education,
Medical, Documents, Events, Notes, Entertainment, Other

Intent should describe why a user might have saved the screenshot.
Examples:
Buy Later, Cook Later, Visit Later, Read Later, Study Later,
Pay Later, Upcoming Travel, Payment Proof, Reference,
Important Document, Event, Other

Return ONLY valid JSON.

Use null when information is not available.

JSON format:

{
  "title": "string",
  "summary": "string",
  "category": "string",
  "intent": "string",
  "keywords": [],
  "entities": [],
  "date": null,
  "price": null,
  "location": null
}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            {
                "text": prompt
            },
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_bytes
                }
            }
        ],
    )

    text = response.text.strip()

    # Remove markdown code fences if the model returns them.
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid JSON: {text}"
        ) from exc