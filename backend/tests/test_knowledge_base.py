from backend.services.knowledge_base import KnowledgeBaseService


kb = KnowledgeBaseService()


def test_load():

    assert kb.entry_count == 3


def test_find_interaction():

    result = kb.find_drug_interaction(
        "Warfarin",
        "Ibuprofen"
    )

    assert result is not None

    assert result["id"] == "KB-001"


def test_reverse_lookup():

    result = kb.find_drug_interaction(
        "Ibuprofen",
        "Warfarin"
    )

    assert result is not None

    assert result["id"] == "KB-001"


def test_unknown():

    result = kb.find_drug_interaction(
        "Paracetamol",
        "Vitamin C"
    )

    assert result is None