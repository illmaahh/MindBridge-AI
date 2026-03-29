import google.generativeai as genai
import os
import json
import asyncio

class MoodAnalysisAgent:
    AGENT_NAME = "mood_analysis_agent"
    AGENT_DESCRIPTION = "Detects emotional state and mood intensity from user text"

    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def run(self, user_message: str) -> dict:
        prompt = f"""You are an empathetic mental wellness AI. Analyze the following message and return ONLY a valid JSON object.

Message: "{user_message}"

Return this exact JSON structure:
{{
  "mood": "one of: happy, sad, anxious, angry, stressed, calm, overwhelmed, hopeful, lonely, confused",
  "intensity": "one of: mild, moderate, high",
  "emotions": ["list", "of", "2-3", "specific", "emotions"],
  "summary": "one empathetic sentence acknowledging their feeling",
  "needs_support": true or false
}}

Only return the JSON. No explanation, no markdown."""

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.model.generate_content(prompt)
            )
            text = response.text.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
        except Exception as e:
            return {
                "mood": "neutral",
                "intensity": "mild",
                "emotions": ["uncertain"],
                "summary": "I'm here to listen and support you.",
                "needs_support": False
            }
