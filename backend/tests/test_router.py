from  reasoning.router import ReasoningRouter


router = ReasoningRouter()


def test_simple_case():

    result = router.decide(
        ["Warfarin"],
        "Ibuprofen",
    )

    assert result.requires_ai is False


def test_polypharmacy():

    result = router.decide(
        [
            "Warfarin",
            "Metformin",
            "Digoxin",
        ],
        "Ibuprofen",
    )

    assert result.requires_ai is True


def test_unknown_drug():

    result = router.decide(
        [],
        "Unknown",
    )

    assert result.requires_ai is True