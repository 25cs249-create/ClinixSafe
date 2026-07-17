from  schemas.core import (
    CommunicationDraft,
    CommunicationType,
    RiskLevel,
    SafetyReport,
)
from  services.slashy_client import SlashyClient


class SlashyService:
    """
    Generates clinician-reviewed communication drafts.

    Workflow:
        SafetyReport
            ↓
        Slashy MCP (when configured)
            ↓
        Fallback local templates
            ↓
        Clinician Review
            ↓
        Manual Send

    The RuleEngine only interacts with this service and is unaware
    of whether drafts come from Slashy MCP or the local fallback.
    """

    def __init__(self):

        self.client = SlashyClient()

    def create_drafts(
        self,
        report: SafetyReport,
    ) -> list[CommunicationDraft]:
        """
        Try Slashy MCP first.

        If Slashy is unavailable or not yet configured,
        fall back to deterministic local templates so the
        application remains fully functional.
        """

        try:
            drafts = self.client.generate_drafts(report)

            if drafts:
                return drafts

        except NotImplementedError:
            pass

        except Exception:
            # Never let partner integration break the
            # medication safety workflow.
            pass

        return [
            self._clinician_summary(report),
            self._patient_summary(report),
            self._follow_up(report),
        ]

    def _clinician_summary(
        self,
        report: SafetyReport,
    ) -> CommunicationDraft:

        recommendations = (
            "\n".join(f"• {item} "for item in report.recommendations)
            if report.recommendations
            else "• No additional recommendations."
        )

        return CommunicationDraft(
            type=CommunicationType.CLINICIAN,
            title="Clinician Summary",
            content=(
                f"Risk Level: {report.riskLevel.value}\n\n"
                f"{report.summary}\n\n"
                "Recommendations:\n"
                f"{recommendations}\n\n"
                "Please review before making any clinical decision."
            ),
        )

    def _patient_summary(
        self,
        report: SafetyReport,
    ) -> CommunicationDraft:

        if report.riskLevel == RiskLevel.SAFE:

            message = (
                "No known medication interaction was identified "
                "based on the current ClinixSafe knowledge base. "
                "Please continue taking medications exactly as "
                "advised by your healthcare professional."
            )

        elif report.riskLevel == RiskLevel.LIMITED:

            message = (
                "The medication could not be fully verified using "
                "the current knowledge base. Please consult your "
                "doctor or pharmacist before taking this medicine."
            )

        else:

            message = (
                "A potential medication safety concern has been "
                "identified. Please speak with your doctor or "
                "pharmacist before starting or continuing this "
                "medication."
            )

        return CommunicationDraft(
            type=CommunicationType.PATIENT,
            title="Patient Explanation",
            content=message,
        )

    def _follow_up(
        self,
        report: SafetyReport,
    ) -> CommunicationDraft:

        if report.riskLevel == RiskLevel.SAFE:

            action = (
                "Continue routine clinical care and document the "
                "verification outcome."
            )

        elif report.riskLevel == RiskLevel.LIMITED:

            action = (
                "Verify the medication details manually before "
                "communicating with the patient."
            )

        else:

            action = (
                "Review the Safety Report, confirm the treatment "
                "plan, and discuss recommendations with the patient."
            )

        return CommunicationDraft(
            type=CommunicationType.FOLLOW_UP,
            title="Recommended Follow-up",
            content=action,
        )