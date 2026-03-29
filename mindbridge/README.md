# 🧠 MindBridge — AI Mental Wellness Agent

> Built with Gemini 1.5 Flash · Google ADK Pattern · Cloud Run

A multi-agent AI wellness companion that listens, analyzes your mood, and recommends personalized wellness activities.

---

## 🏗️ Architecture (ADK Multi-Agent Pattern)

```
User Message
     │
     ▼
┌─────────────────────────────────┐
│     MindBridge Orchestrator     │  ← Routes to right agents
└─────────────────────────────────┘
     │              │              │
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Mood    │  │ Recommend│  │ Journal  │
│  Agent   │  │  Agent   │  │  Agent   │
└──────────┘  └──────────┘  └──────────┘
     │              │              │
     └──────────────┴──────────────┘
                    │
                    ▼
             ┌──────────┐
             │ Insights │
             │  Agent   │
             └──────────┘
```

---

## 🚀 Local Setup (Step by Step)

### Step 1 — Clone and Install

```bash
git clone <your-repo-url>
cd mindbridge
pip install -r requirements.txt
```

### Step 2 — Get Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 3 — Set Environment Variable

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Step 4 — Run Locally

```bash
python main.py
```
Open http://localhost:8080

---

## ☁️ Deploy to Google Cloud Run

### Prerequisites
- Google Cloud account (free tier works!)
- Google Cloud CLI installed: https://cloud.google.com/sdk/docs/install

### Step 1 — Login and Setup

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2 — Deploy with One Command

```bash
gcloud run deploy mindbridge \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here \
  --memory 512Mi \
  --cpu 1
```

### Step 3 — Get Your URL

After deployment, you'll see:
```
Service URL: https://mindbridge-xxxxx-uc.a.run.app
```

That's your submission URL! ✅

---

## 📁 Project Structure

```
mindbridge/
├── main.py                    # FastAPI app + API routes
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py        # Multi-agent coordinator (ADK pattern)
│   ├── mood_agent.py          # Mood detection agent
│   ├── recommendation_agent.py # Wellness recommendation agent
│   ├── journal_agent.py       # Deep journal analysis agent
│   └── insights_agent.py      # Weekly pattern insights agent
├── templates/
│   └── index.html             # Frontend UI
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## ✨ Features

- 🧠 **Mood Analysis** — 10 emotion types with intensity levels
- 💡 **Personalized Recommendations** — Activities tailored to your mood
- 📓 **Journal Analysis** — Deep emotional pattern recognition
- 📊 **Weekly Insights** — Wellbeing score + trend analysis
- 🎨 **Beautiful Dark UI** — Mobile-friendly design
- ⚡ **Multi-Agent Pipeline** — ADK orchestrator pattern

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main UI |
| POST | `/api/chat` | Chat + mood analysis |
| POST | `/api/journal` | Journal analysis |
| GET | `/api/history/{session_id}` | Mood history |
| GET | `/api/insights/{session_id}` | Weekly insights |
| GET | `/health` | Health check |
