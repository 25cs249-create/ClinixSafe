from backend.schemas.core import (
    RiskLevel,
    EvidenceStrength,
    SafetyReport,
    EvidenceTrace,
)
from backend.services.knowledge_base import KnowledgeBaseService


class RuleEngine:

    def __init__(self):

        self.kb = KnowledgeBaseService()

    def analyze(self, current_medications: list[str], new_medication: str):

        for medication in current_medications:

            match = self.kb.find_drug_interaction(
                medication,
                new_medication,
            )

            if match:

                trace = EvidenceTrace(
                    evidenceId=match["id"],
                    title="Drug Interaction",
                    description=match["mechanism"],
                    source=match["citations"][0],
                    sourceType="GUIDELINE",
                    priority="HIGH",
                )

                return SafetyReport(
                    analysisVersion="1.0.0",
                    knowledgeBaseVersion=self.kb.version,
                    riskLevel=RiskLevel(match["severity"]),
                    evidenceStrength=EvidenceStrength(match["evidenceStrength"]),
                    summary=match["recommendation"],
                    recommendations=[match["recommendation"]],
                    evidenceTrace=[trace],
                )

        return SafetyReport(
            analysisVersion="1.0.0",
            knowledgeBaseVersion=self.kb.version,
            riskLevel=RiskLevel.SAFE,
            evidenceStrength=EvidenceStrength.HIGH,
            summary="No known interaction detected.",
            recommendations=["Safe based on current knowledge base."],
        )