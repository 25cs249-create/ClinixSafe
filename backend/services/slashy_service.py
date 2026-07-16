from backend.schemas.core import (
    CommunicationDraft,
    CommunicationType,
    RiskLevel,
    SafetyReport,
)


class SlashyService:
    """
    Generates draft communications from a completed SafetyReport.

    This service does NOT send messages.
    It only prepares drafts for clinician review.

    Future enhancement:
    Replace the template generation with Slashy MCP while
    preserving the same public interface.
    """

    def create_drafts(
        self,
        report: SafetyReport,
    ) -> list[CommunicationDraft]:

        return [
            self._clinician_summary(report),
            self._patient_summary(report),
            self._follow_up(report),
        ]

    def _clinician_summary(
        self,
        report: SafetyReport,
    ) -> CommunicationDraft:

        return CommunicationDraft(
            type=CommunicationType.CLINICIAN,
            title="Clinician Summary",
            content=(
                f"Risk Level: {report.riskLevel.value}\n\n"
                f"{report.summary}\n\n"
                "Review the recommendations before making any "
                "clinical decision."
            ),
        )

    def _patient_summary(
        self,
        report: SafetyReport,
    ) -> CommunicationDraft:

        if report.riskLevel == RiskLevel.SAFE:
            message = (
                "No known medication interaction was identified "
                "based on the current knowledge base."
            )

        elif report.riskLevel == RiskLevel.LIMITED:
            message = (
                "The medication could not be fully verified. "
                "Please consult your healthcare professional "
                "before taking this medicine."
            )

        else:
            message = (
                "A possible medication safety concern was identified. "
                "Please speak with your healthcare professional "
                "before starting this medication."
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

        return CommunicationDraft(
            type=CommunicationType.FOLLOW_UP,
            title="Recommended Follow-up",
            content=(
                "Review the Safety Report and confirm the clinical "
                "plan before communicating with the patient."
            ),
        )