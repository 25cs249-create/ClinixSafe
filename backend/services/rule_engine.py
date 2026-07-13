from backend.schemas.core import (
    RiskLevel,
    EvidenceStrength,
    SafetyReport,
    EvidenceTrace,
)
from backend.services.alias_resolver import AliasResolver
from backend.services.knowledge_base import KnowledgeBaseService


class RuleEngine:

    def __init__(self):

        self.kb = KnowledgeBaseService()
        self.resolver = AliasResolver()

    def analyze(self, current_medications: list[str], new_medication: str):

        resolved_current = [
            self.resolver.resolve(medication)
            for medication in current_medications
        ]
        resolved_new = self.resolver.resolve(new_medication)

        for medication in resolved_current:

            match = self.kb.find_drug_interaction(
                medication,
                resolved_new,
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