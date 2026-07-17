from  schemas.core import (
    CommunicationDraft,
    SafetyReport,
)


class SlashyClient:
    """
    Client for communicating with Slashy.

    This class is intentionally isolated from the Rule Engine so that
    partner integration can be added without changing ClinixSafe's
    clinical workflow.

    Current implementation:
        • Placeholder interface

    Future implementation:
        • Connect to the official Slashy MCP/API
        • Submit the completed SafetyReport
        • Receive clinician-reviewed communication drafts

    This client NEVER performs medication analysis.
    It only handles communication generation.
    """

    def generate_drafts(
        self,
        report: SafetyReport,
    ) -> list[CommunicationDraft]:
        """
        Generate communication drafts using Slashy.

        Raises:
            NotImplementedError:
                Until the official Slashy integration is available.
        """
        raise NotImplementedError(
            "Slashy integration has not been configured."
        )