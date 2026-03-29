import google.generativeai as genai
import os
import json
import asyncio
from collections import Counter

class InsightsAgent:
    AGENT_NAME = "insights_agent"
    AGENT_DESCRIPTION = "Generates weekly emotional pattern insights from mood history"

    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate(self, mood_history: list) -> dict:
        if not mood_history:
            return {
                "summary": "Start chatting to build your mood history and unlock insights!",
                "patterns": [],
                "dominant_mood": "unknown",
                "wellbeing_score": 0,
                "positive_highlight": "",
                "gentle_suggestion": "Begin your wellness journey today."
            }

        moods = [e.get("mood", "neutral") for e in mood_history]
        dominant_mood = Counter(moods).most_common(1)[0][0]
        positive_moods = {"happy", "calm", "hopeful"}
        score = round(sum(1 for m in moods if m in positive_moods) / len(moods) * 100)

        prompt = f"""Analyze this mood history and return ONLY valid JSON:
Mood history (last 10): {json.dumps(mood_history[-10:])}
Dominant mood: {dominant_mood}
Wellbeing score: {score}/100

{{
  "summary": "2-3 sentence warm summary of their emotional week",
  "patterns": ["pattern 1 observed", "pattern 2 observed"],
  "positive_highlight": "One positive thing noticed in their journey",
  "gentle_suggestion": "One actionable suggestion for the coming week",
  "dominant_mood": "{dominant_mood}",
  "wellbeing_score": {score}
}}

Only return JSON."""

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
            result = json.loads(text.strip())
            result["dominant_mood"] = dominant_mood
            result["wellbeing_score"] = score
            return result
        except Exception:
            return {
                "summary": f"You've logged {len(mood_history)} check-ins. Your dominant mood has been {dominant_mood}.",
                "patterns": ["Regular check-ins show self-awareness", "Emotional variety is normal and healthy"],
                "positive_highlight": "You're showing up for yourself by tracking your wellness.",
                "gentle_suggestion": "Try a 5-minute morning mood check-in tomorrow.",
                "dominant_mood": dominant_mood,
                "wellbeing_score": score
            }
