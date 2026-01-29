from fastapi import FastAPI
from app.models import Event
from app.services.enrich import enrich_event
from app.services.llm import generate_recommendation

app = FastAPI(title="AI Ops Copilot", version="0.1")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/event")
def receive_event(event: Event):
    enriched = enrich_event(event)
    ai = generate_recommendation(enriched)
    return {
        "received": True,
        "event_type": event.event_type,
        "event_id": event.event_id,
        "enriched": enriched,
        "ai": ai
    }



