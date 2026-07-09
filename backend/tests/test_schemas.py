from backend.schemas.core import (
    RiskLevel,
    EvidenceStrength,
    SafetyReport,
)


def test_create_report():

    report = SafetyReport(
        analysisVersion="1.0.0",
        knowledgeBaseVersion="1.0.0",
        riskLevel=RiskLevel.SAFE,
        evidenceStrength=EvidenceStrength.HIGH,
        summary="Everything looks good."
    )

    assert report.reportId.startswith("REP-")

    assert report.riskLevel == RiskLevel.SAFE