from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from agents.orchestrator import MindBridgeOrchestrator

app = FastAPI(title="MindBridge - AI Wellness Agent")

# ✅ Templates (correct if Root Directory = mindbridge in Render)
templates = Jinja2Templates(directory="templates")

orchestrator = MindBridgeOrchestrator()

# -------------------------------
# Request Models
# -------------------------------
class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"

class JournalRequest(BaseModel):
    entry: str
    session_id: str = "default"

# -------------------------------
# Routes
# -------------------------------

# ✅ Homepage (fixes your 405 issue)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat API
@app.post("/api/chat")
async def chat(req: MessageRequest):
    result = await orchestrator.process_message(req.message, req.session_id)
    return JSONResponse(result)

# Journal API
@app.post("/api/journal")
async def journal(req: JournalRequest):
    result = await orchestrator.analyze_journal(req.entry, req.session_id)
    return JSONResponse(result)

# Mood history
@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    history = orchestrator.get_mood_history(session_id)
    return JSONResponse({"history": history})

# Insights
@app.get("/api/insights/{session_id}")
async def get_insights(session_id: str):
    insights = await orchestrator.get_insights(session_id)
    return JSONResponse(insights)

# Health check (useful for Render)
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "MindBridge"}

# -------------------------------
# Run Server (FIXED FOR RENDER)
# -------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))  # ✅ important fix
    uvicorn.run("main:app", host="0.0.0.0", port=port)