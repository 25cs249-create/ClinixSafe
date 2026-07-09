from backend.services.rule_engine import RuleEngine
from backend.schemas.core import RiskLevel


engine = RuleEngine()


def test_high_risk():

    report = engine.analyze(
        ["Warfarin"],
        "Ibuprofen"
    )

    assert report.riskLevel == RiskLevel.HIGH

    assert len(report.evidenceTrace) == 1


def test_safe_case():

    report = engine.analyze(
        ["Vitamin C"],
        "Paracetamol"
    )

    assert report.riskLevel == RiskLevel.SAFE