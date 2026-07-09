from fastapi import FastAPI

from backend.settings import get_settings
from backend.services.knowledge_base import KnowledgeBaseService
from backend.services.rule_engine import RuleEngine
from backend.validation.firewall import AIFirewall
from backend.api.models import AnalyzeRequest

# -------------------------------------------------
# Settings
# -------------------------------------------------

settings = get_settings()

# -------------------------------------------------
# Services
# -------------------------------------------------

kb = KnowledgeBaseService()

engine = RuleEngine()

firewall = AIFirewall()

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI(
    title="ClinixSafe API",
    version=settings.engine_version,
)

# -------------------------------------------------
# Routes
# -------------------------------------------------

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
        "demo_mode": settings.demo_mode,
    }


@app.get("/demo/high-risk")
def demo_high_risk():
    report = engine.analyze(
        ["Warfarin"],
        "Ibuprofen",
    )

    return report


@app.post("/api/v1/analyze")
def analyze(request: AnalyzeRequest):

    report = engine.analyze(
        request.currentMedications,
        request.newMedication,
    )

    report = firewall.validate(report)

    return report