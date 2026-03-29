"""
MindBridge Orchestrator — Multi-Agent Pipeline (ADK Pattern)

This is the heart of the ADK architecture:
  1. MoodAnalysisAgent  → understands emotional state
  2. RecommendationAgent → generates personalized wellness actions
  3. JournalAgent        → deep journal entry analysis
  4. InsightsAgent       → weekly pattern recognition

The Orchestrator routes messages to the right agents and
combines their outputs into a unified response.
"""

from datetime import datetime
from agents.mood_agent import MoodAnalysisAgent
from agents.recommendation_agent import RecommendationAgent
from agents.journal_agent import JournalAgent
from agents.insights_agent import InsightsAgent

class MindBridgeOrchestrator:

    def __init__(self):
        # Initialize all sub-agents
        self.mood_agent = MoodAnalysisAgent()
        self.recommendation_agent = RecommendationAgent()
        self.journal_agent = JournalAgent()
        self.insights_agent = InsightsAgent()

        # In-memory session storage (replace with Firestore in production)
        self.sessions: dict[str, list] = {}

    def _get_session(self, session_id: str) -> list:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    async def process_message(self, message: str, session_id: str) -> dict:
        """
        Main pipeline:
        message → MoodAgent → RecommendationAgent → combined response
        """
        session = self._get_session(session_id)

        # Step 1: Analyze mood
        mood_data = await self.mood_agent.run(message)

        # Step 2: Generate recommendations based on mood
        recommendations = await self.recommendation_agent.run(mood_data, message)

        # Step 3: Store in session history
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "mood": mood_data.get("mood", "neutral"),
            "intensity": mood_data.get("intensity", "mild"),
            "emotions": mood_data.get("emotions", []),
        }
        session.append(entry)

        return {
            "mood_data": mood_data,
            "recommendations": recommendations,
            "session_count": len(session),
            "timestamp": entry["timestamp"]
        }

    async def analyze_journal(self, entry: str, session_id: str) -> dict:
        """Deep journal analysis pipeline."""
        session = self._get_session(session_id)

        # Journal agent does the deep analysis
        analysis = await self.journal_agent.analyze(entry)

        # Also run mood detection to log it
        mood_data = await self.mood_agent.run(entry)

        # Store in history
        session.append({
            "timestamp": datetime.now().isoformat(),
            "message": entry[:100] + "..." if len(entry) > 100 else entry,
            "mood": mood_data.get("mood", "neutral"),
            "intensity": mood_data.get("intensity", "mild"),
            "emotions": mood_data.get("emotions", []),
            "type": "journal"
        })

        return {
            "analysis": analysis,
            "mood_data": mood_data,
            "timestamp": datetime.now().isoformat()
        }

    def get_mood_history(self, session_id: str) -> list:
        """Return mood history for a session."""
        return self._get_session(session_id)

    async def get_insights(self, session_id: str) -> dict:
        """Generate insights from mood history."""
        history = self._get_session(session_id)
        return await self.insights_agent.generate(history)
