from  schemas.core import (
    RiskLevel,
    EvidenceStrength,
    SafetyReport,
    EvidenceTrace,
)
from  services.alias_resolver import AliasResolver
from  services.knowledge_base import KnowledgeBaseService
from  services.slashy_service import SlashyService


class RuleEngine:

    def __init__(self):

        self.kb = KnowledgeBaseService()
        self.resolver = AliasResolver()
        self.slashy = SlashyService()

    def _limited_report(self, medication_name: str) -> SafetyReport:
        """
        Return a LIMITED safety report for medications that cannot
        be verified using the current knowledge base.
        """
        report = SafetyReport(
            analysisVersion="1.0.0",
            knowledgeBaseVersion=self.kb.version,
            riskLevel=RiskLevel.LIMITED,
            evidenceStrength=EvidenceStrength.LIMITED,
            summary=(
                f"Medication '{medication_name}' could not be verified "
                "using the current ClinixSafe knowledge base. "
                "Manual clinical review is recommended before prescribing."
            ),
            recommendations=[
                "Verify the medication name and perform a manual clinical review before prescribing."
            ],
            warnings=[
                "Medication could not be verified."
            ],
        )

        report.communicationDrafts = self.slashy.create_drafts(report)

        return report

    def analyze(
        self,
        current_medications: list[str],
        new_medication: str,
    ) -> SafetyReport:

        resolved_current = [
            (
                original,
                self.resolver.resolve(original),
            )
            for original in current_medications
        ]

        resolved_new = self.resolver.resolve(new_medication)

        # --------------------------------------------------
        # Phase 10
        # Unknown medication detection
        # --------------------------------------------------

        if not self.kb.is_known(resolved_new):
            return self._limited_report(new_medication)

        for original_medication, resolved_medication in resolved_current:

            if not self.kb.is_known(resolved_medication):
                return self._limited_report(original_medication)

            match = self.kb.find_drug_interaction(
                resolved_medication,
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

                report = SafetyReport(
                    analysisVersion="1.0.0",
                    knowledgeBaseVersion=self.kb.version,
                    riskLevel=RiskLevel(match["severity"]),
                    evidenceStrength=EvidenceStrength(
                        match["evidenceStrength"]
                    ),
                    summary=match["recommendation"],
                    recommendations=[
                        match["recommendation"]
                    ],
                    evidenceTrace=[trace],
                )

                report.communicationDrafts = (
                    self.slashy.create_drafts(report)
                )

                return report

        report = SafetyReport(
            analysisVersion="1.0.0",
            knowledgeBaseVersion=self.kb.version,
            riskLevel=RiskLevel.SAFE,
            evidenceStrength=EvidenceStrength.HIGH,
            summary="No known interaction detected.",
            recommendations=[
                "Safe based on current knowledge base."
            ],
        )

        report.communicationDrafts = (
            self.slashy.create_drafts(report)
        )

        return report