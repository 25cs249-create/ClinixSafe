from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.settings import get_settings
from backend.services.knowledge_base import KnowledgeBaseService
from backend.services.rule_engine import RuleEngine
from backend.validation.firewall import AIFirewall
from backend.api.models import AnalyzeRequest
from backend.reasoning.router import ReasoningRouter

router = ReasoningRouter()
settings = get_settings()
kb = KnowledgeBaseService()
engine = RuleEngine()
firewall = AIFirewall()

app = FastAPI(
    title="ClinixSafe API",
    version=settings.engine_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    decision = router.decide(
        request.currentMedications,
        request.newMedication,
    )
    print(
        f"Routing: {decision.reason} | AI Required: {decision.requires_ai}"
    )
    report = firewall.validate(report)

    return report