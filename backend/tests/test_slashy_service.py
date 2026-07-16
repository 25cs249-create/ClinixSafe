from backend.schemas.core import (
    CommunicationType,
    EvidenceStrength,
    RiskLevel,
    SafetyReport,
)
from backend.services.slashy_service import SlashyService


service = SlashyService()


def _report(level: RiskLevel) -> SafetyReport:
    return SafetyReport(
        analysisVersion="1.0.0",
        knowledgeBaseVersion="1.2.0",
        riskLevel=level,
        evidenceStrength=EvidenceStrength.HIGH,
        summary="Test summary",
    )


def test_creates_three_drafts():

    drafts = service.create_drafts(
        _report(RiskLevel.HIGH)
    )

    assert len(drafts) == 3


def test_contains_clinician_summary():

    drafts = service.create_drafts(
        _report(RiskLevel.HIGH)
    )

    assert drafts[0].type == CommunicationType.CLINICIAN
    assert drafts[0].reviewRequired is True


def test_contains_patient_summary():

    drafts = service.create_drafts(
        _report(RiskLevel.HIGH)
    )

    assert drafts[1].type == CommunicationType.PATIENT
    assert drafts[1].reviewRequired is True


def test_contains_follow_up():

    drafts = service.create_drafts(
        _report(RiskLevel.HIGH)
    )

    assert drafts[2].type == CommunicationType.FOLLOW_UP
    assert drafts[2].reviewRequired is True


def test_safe_message():

    drafts = service.create_drafts(
        _report(RiskLevel.SAFE)
    )

    assert "No known medication interaction" in drafts[1].content


def test_limited_message():

    drafts = service.create_drafts(
        _report(RiskLevel.LIMITED)
    )

    assert "could not be fully verified" in drafts[1].content


def test_high_message():

    drafts = service.create_drafts(
        _report(RiskLevel.HIGH)
    )

    assert "medication safety concern" in drafts[1].content