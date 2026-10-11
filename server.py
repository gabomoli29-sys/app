from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import datetime

app = FastAPI(title="Cronos AI API", version="1.0.0")

class TaskItem(BaseModel):
    id: Optional[int] = None
    title: str
    due_date: str
    source: str
    completed: bool = False

db_tasks: List[TaskItem] = [
    TaskItem(id=1, title="Preparar notas EA-112 Holland-Rubin", due_date="2025-05-14T15:00:00", source="Minerva"),
    TaskItem(id=2, title="Física Cuántica: Guía Schrödinger", due_date="2025-05-15T09:00:00", source="Classroom"),
]

@app.get("/")
def root():
    return {"status": "online", "app": "Cronos AI API", "portal": "app.minervaproject.com"}

@app.get("/api/tasks", response_model=List[TaskItem])
def get_tasks():
    return db_tasks

@app.post("/api/webhook/google-assistant")
def handle_assistant_intent(payload: dict):
    query_text = payload.get("queryResult", {}).get("queryText", "")
    new_task = TaskItem(
        id=len(db_tasks) + 1,
        title=query_text or "Nuevo recordatorio por voz",
        due_date=datetime.datetime.now().isoformat(),
        source="Assistant"
    )
    db_tasks.append(new_task)
    return {
        "fulfillmentText": f"¡Listo! Cronos AI guardó tu recordatorio: '{new_task.title}'",
        "task_id": new_task.id
    }

@app.get("/api/minerva/sync")
def sync_minerva():
    return {
        "portal_url": "https://app.minervaproject.com/home/student",
        "student_account": "sofia.alvarez@minerva.edu",
        "sync_status": "synced",
        "active_hcs": ["#hypothesis", "#sourcequality", "#systemdynamics"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)