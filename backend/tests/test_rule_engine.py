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
        ["Warfarin"],
        "Crocin"
    )

    assert report.riskLevel == RiskLevel.SAFE


# --------------------------------------------------
# Phase 10
# Unknown medication detection
# --------------------------------------------------

def test_unknown_new_medication_returns_limited():

    report = engine.analyze(
        ["Warfarin"],
        "Zylofexamine"
    )

    assert report.riskLevel == RiskLevel.LIMITED

    assert "could not be verified" in report.summary.lower()

    assert report.evidenceTrace == []


def test_unknown_current_medication_returns_limited():

    report = engine.analyze(
        ["Zylofexamine"],
        "Ibuprofen"
    )

    assert report.riskLevel == RiskLevel.LIMITED

    assert "could not be verified" in report.summary.lower()

    assert report.evidenceTrace == []


# --------------------------------------------------
# Phase 9 regression
# Alias resolution
# --------------------------------------------------

def test_brand_name_without_interaction_returns_safe():

    report = engine.analyze(
        ["Warfarin"],
        "Crocin"
    )

    assert report.riskLevel == RiskLevel.SAFE


def test_brand_name_interaction_returns_high():

    report = engine.analyze(
        ["Warfarin"],
        "Combiflam"
    )

    assert report.riskLevel == RiskLevel.HIGH

    assert len(report.evidenceTrace) == 1