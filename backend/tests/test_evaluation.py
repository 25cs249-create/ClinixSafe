from backend.evaluation.runner import load_dataset


def test_dataset_loads():

    dataset = load_dataset()

    assert len(dataset) > 0


def test_first_case_exists():

    dataset = load_dataset()

    assert dataset[0]["id"] == "CASE-001"