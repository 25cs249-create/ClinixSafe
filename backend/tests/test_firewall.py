import pytest

from backend.validation.firewall import AIFirewall
from backend.schemas.core import (
    SafetyReport,
    RiskLevel,
    EvidenceStrength,
)

firewall = AIFirewall()


def test_valid_report_passes():

    report = SafetyReport(
        analysisVersion="1.0.0",
        knowledgeBaseVersion="1.0.0",
        riskLevel=RiskLevel.HIGH,
        evidenceStrength=EvidenceStrength.HIGH,
        summary="Test",
        evidenceTrace=[
            {
                "evidenceId": "KB-001",
                "title": "Test",
                "description": "Test",
                "source": "FDA",
                "sourceType": "GUIDELINE",
                "priority": "HIGH",
            }
        ],
    )

    validated = firewall.validate(report)

    assert validated.riskLevel == RiskLevel.HIGH


def test_high_without_evidence_fails():

    report = SafetyReport(
        analysisVersion="1.0.0",
        knowledgeBaseVersion="1.0.0",
        riskLevel=RiskLevel.HIGH,
        evidenceStrength=EvidenceStrength.HIGH,
        summary="Test",
        evidenceTrace=[],
    )

    with pytest.raises(ValueError):
        firewall.validate(report)