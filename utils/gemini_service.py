import json
import re
from typing import Any
from google import genai
from utils.config import GEMINI_API_KEY

class GeminiService:
    def __init__(self, service_prompt):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.prompt = service_prompt

    def get_response(self) -> dict[str, str] | Any:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=self.prompt,
            )

            text = response.text.strip() if hasattr(response, "text") else ""

            if not text and hasattr(response, "candidates"):
                text = response.candidates[0].content.parts[0].text.strip()

            cleaned = re.sub(r"^```(?:json)?|```$", "", text, flags=re.IGNORECASE).strip()
            return json.loads(cleaned)

        except ValueError as vl:
            return {"status": "error", "code": 400, "response": f"Invalid JSON response {str(vl)}"}

        except ConnectionError:
            return {"status": "error", "code": 400, "response": "Connection error"}

        except Exception as e:
            return {"status": "error", "code": 400, "response": str(e)}

prompt = """Hello Gemini! 
Please respond with a JSON matching this structure:
and choose a topic from yourself and update the title in repone to be it, bullet_points should be about that topic
```json
{
  "status": "ok",
  "code": 200,
  "response": " {{
    "title": "Introduction",
    "bullet_points": [
      "Definition",
      "Importance",
      "Brief history"
    ]
  }}",
}
```"""

obj = GeminiService(service_prompt=prompt)
print(obj.get_response())