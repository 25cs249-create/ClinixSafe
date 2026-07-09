from fastapi import FastAPI

from backend.settings import get_settings

settings = get_settings()

from backend.services.knowledge_base import KnowledgeBaseService

kb = KnowledgeBaseService()

app = FastAPI(
    title="ClinixSafe API",
    version=settings.engine_version
)


@app.get("/")
def root():
    return {
        "message": "ClinixSafe Backend Running"
    }


@app.get("/health")
def health():

    return {
        "status": "operational",
        "engine_version": settings.engine_version,
        "knowledge_base_version": kb.version,
        "knowledge_entries": kb.entry_count,
        "demo_mode": settings.demo_mode
    }