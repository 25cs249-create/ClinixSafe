from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_analyze_high():

    response = client.post(
        "/api/v1/analyze",
        json={
            "currentMedications": [
                "Warfarin"
            ],
            "newMedication": "Ibuprofen"
        },
    )

    assert response.status_code == 200

    assert response.json()["riskLevel"] == "HIGH"


def test_analyze_safe():

    response = client.post(
        "/api/v1/analyze",
            json={
    "currentMedications": [
        "Warfarin"
    ],
    "newMedication": "Crocin"
    }
    )

    assert response.status_code == 200

    assert response.json()["riskLevel"] == "SAFE"