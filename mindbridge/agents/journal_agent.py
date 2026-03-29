import google.generativeai as genai
import os
import json
import asyncio

class JournalAgent:
    AGENT_NAME = "journal_analysis_agent"
    AGENT_DESCRIPTION = "Deep emotional analysis of journal entries"

    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analyze(self, journal_entry: str) -> dict:
        prompt = f"""You are a compassionate AI wellness guide. Analyze this journal entry:
"{journal_entry}"

Return ONLY a valid JSON object:
{{
  "emotional_themes": ["list of 2-4 key emotional themes"],
  "strengths_shown": ["list of 2-3 personal strengths visible in the writing"],
  "gentle_observations": ["list of 2-3 kind, non-judgmental observations"],
  "growth_opportunities": ["list of 2 areas to explore for personal growth"],
  "response": "A warm 3-4 sentence response acknowledging their experience",
  "next_journal_prompts": [
    "A follow-up question to explore deeper",
    "A question focused on solutions",
    "A gratitude-based question"
  ],
  "professional_note": "Gentle reminder about professional support if needed, or empty string"
}}

Be compassionate. Never diagnose. Only return JSON."""

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
        except Exception:
            return {
                "emotional_themes": ["reflection", "self-awareness"],
                "strengths_shown": ["courage to express feelings", "self-reflection"],
                "gentle_observations": ["You are taking time to understand yourself."],
                "growth_opportunities": ["Exploring what you need right now", "Building a daily check-in habit"],
                "response": "Thank you for sharing this. Writing your feelings is a powerful act of self-care.",
                "next_journal_prompts": [
                    "What do you need most right now?",
                    "What is one small step forward you could take?",
                    "What are you grateful for today, even if small?"
                ],
                "professional_note": ""
            }
