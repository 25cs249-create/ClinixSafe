from backend.schemas.core import SafetyReport


class AIFirewall:

    def validate(self, report: SafetyReport) -> SafetyReport:

        if report.riskLevel in ["HIGH", "CONTRAINDICATED"]:

            if len(report.evidenceTrace) == 0:
                raise ValueError(
                    "High-risk reports must include evidence."
                )

        return report