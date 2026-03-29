from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from agents.orchestrator import MindBridgeOrchestrator

app = FastAPI(title="MindBridge - AI Wellness Agent")

templates = Jinja2Templates(directory="templates")

orchestrator = MindBridgeOrchestrator()

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"

class JournalRequest(BaseModel):
    entry: str
    session_id: str = "default"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat(req: MessageRequest):
    """Main chat endpoint — mood analysis + recommendations."""
    result = await orchestrator.process_message(req.message, req.session_id)
    return JSONResponse(result)

@app.post("/api/journal")
async def journal(req: JournalRequest):
    """Deep journal analysis endpoint."""
    result = await orchestrator.analyze_journal(req.entry, req.session_id)
    return JSONResponse(result)

@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    """Get mood history for a session."""
    history = orchestrator.get_mood_history(session_id)
    return JSONResponse({"history": history})

@app.get("/api/insights/{session_id}")
async def get_insights(session_id: str):
    """Get weekly emotional pattern insights."""
    insights = await orchestrator.get_insights(session_id)
    return JSONResponse(insights)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "MindBridge"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
