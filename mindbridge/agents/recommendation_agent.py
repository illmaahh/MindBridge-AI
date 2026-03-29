import google.generativeai as genai
import os
import json
import asyncio

class RecommendationAgent:
    AGENT_NAME = "recommendation_agent"
    AGENT_DESCRIPTION = "Generates personalized wellness activities based on mood"

    ACTIVITY_MAP = {
        "happy":       ["Share your joy with someone", "Start a gratitude journal", "Try a creative hobby"],
        "sad":         ["5-minute breathing exercise", "Watch a comfort show", "Write your feelings down"],
        "anxious":     ["Box breathing (4-4-4-4)", "5-4-3-2-1 grounding technique", "Take a short walk"],
        "angry":       ["Progressive muscle relaxation", "Write an unsent letter", "Physical exercise"],
        "stressed":    ["Pomodoro break (5 min rest)", "Make a priority list", "Drink water & stretch"],
        "calm":        ["Meditation session", "Read something inspiring", "Plan a creative project"],
        "overwhelmed": ["Break tasks into tiny steps", "Ask for help", "One thing at a time"],
        "hopeful":     ["Set a small achievable goal", "Vision board journaling", "Share your plans"],
        "lonely":      ["Reach out to one person", "Join an online community", "Self-compassion meditation"],
        "confused":    ["Brain dump journaling", "Talk it out with someone", "Take a break and return fresh"],
        "neutral":     ["Daily check-in journal", "Stretch for 5 minutes", "Set a positive intention"],
    }

    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def run(self, mood_data: dict, original_message: str) -> dict:
        mood      = mood_data.get("mood", "neutral")
        intensity = mood_data.get("intensity", "mild")
        emotions  = mood_data.get("emotions", [])

        prompt = f"""You are a compassionate wellness coach AI. A user is feeling {mood} ({intensity} intensity).
Their emotions: {', '.join(emotions)}.
Their message: "{original_message}"

Return ONLY a valid JSON object:
{{
  "response": "A warm, empathetic 2-3 sentence response to the user",
  "activities": [
    {{"title": "Activity Name", "description": "How to do it in 1 sentence", "duration": "X minutes", "emoji": "relevant emoji"}},
    {{"title": "Activity Name", "description": "How to do it in 1 sentence", "duration": "X minutes", "emoji": "relevant emoji"}},
    {{"title": "Activity Name", "description": "How to do it in 1 sentence", "duration": "X minutes", "emoji": "relevant emoji"}}
  ],
  "affirmation": "One powerful positive affirmation for them",
  "journal_prompt": "One reflective journaling question to help them process their feelings"
}}

Only return JSON. Be warm, never clinical."""

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
            activities = self.ACTIVITY_MAP.get(mood, self.ACTIVITY_MAP["neutral"])
            return {
                "response": f"I hear you. Feeling {mood} is completely valid. Here are some things that might help.",
                "activities": [
                    {"title": a, "description": "Try this when you're ready.", "duration": "5 minutes", "emoji": "✨"}
                    for a in activities
                ],
                "affirmation": "You are doing better than you think.",
                "journal_prompt": "What is one small thing that could make today a little better?"
            }
