import base64
import json
from typing import Type
from pydantic import BaseModel
from google import genai
from google.genai import types
from ..config import get_settings
from ..models import RecommendationResponse

class GeminiService:
    def __init__(self):
        self.settings = get_settings()
        self.client = genai.Client(api_key=self.settings.gemini_api_key) if self.settings.gemini_api_key else None

    @property
    def available(self):
        return bool(self.settings.ai_enabled and self.client and self.settings.gemini_api_key)

    def _prompt(self, planner: str, payload: dict) -> str:
        return f"""You are PocketSmart AI, a budget recommendation assistant for India.\nPlanner: {planner}\nUser input JSON:\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n\nGenerate practical recommendations. Respect the user's budget. Prices are estimates unless grounded by a real source. Never claim a product is currently in stock or that a price is live. Use platform names only when relevant. Return concise, useful reasons.\n"""

    def generate(self, planner: str, payload: dict, image_bytes: bytes | None = None, mime_type: str | None = None) -> RecommendationResponse:
        if not self.available:
            raise RuntimeError("Gemini is not configured")
        contents = [self._prompt(planner, payload)]
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type or "image/jpeg"))
            contents.append("Analyze the outfit image for color/style coordination, but do not identify the person.")
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecommendationResponse,
                temperature=0.3,
                max_output_tokens=3000,
            ),
        )
        if getattr(response, "parsed", None):
            result = response.parsed
            return result if isinstance(result, RecommendationResponse) else RecommendationResponse.model_validate(result)
        text = getattr(response, "text", "")
        return RecommendationResponse.model_validate_json(text)
