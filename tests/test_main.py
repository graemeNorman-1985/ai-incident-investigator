
from fastapi.testclient import TestClient

from ai_incident_investigator.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_analyse_incident():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "2026-10-09T10:00:03Z ERROR payment-service Payment request failed\n"
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed\n"
        "2026-10-09T10:00:05Z INFO api-gateway Request completed"
    )

    response = client.post(
        "/analyse",
        json={"log_text": logs},
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Found 3 error entries across 2 services.",
        "error_count": 3,
        "entries_by_service": {
            "payment-service": 3,
            "api-gateway": 2,
        },
        "earliest_error": (
            "2026-10-09T10:00:02Z ERROR "
            "payment-service Database connection timeout"
        ),
        "supporting_evidence": [
            "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout",
            "2026-10-09T10:00:03Z ERROR payment-service Payment request failed",
            "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed",
        ],        
    }

# def test_analyse_incident():
#     response = client.post(
#         "/analyse",
#         json={
#             "log_text": "ERROR payment-service: Database connection timeout"
#         },
#     )

#     assert response.status_code == 200

#     data = response.json()

#     assert data["summary"] == (
#         "Analysis received. Automated diagnosis is not implemented yet."
#     )
#     assert data["log_character_count"] == len(
#         "ERROR payment-service: Database connection timeout"
#     )


def test_analyse_rejects_empty_log_text():
    response = client.post(
        "/analyse",
        json={"log_text": ""},
    )

    assert response.status_code == 422


def test_analyse_handles_out_of_order_timestamps_and_malformed_lines():
    logs = (
        "2026-10-09T10:00:05Z ERROR payment-service Payment failed\n"
        "not-a-valid-entry ERROR\n"
        "2026-10-09T10:00:02Z ERROR database-service Connection lost\n"
        "2026-10-09T10:00:03Z INFO api-gateway Request received"
    )

    response = client.post(
        "/analyse",
        json={"log_text": logs},
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Found 2 error entries across 3 services.",
        "error_count": 2,
        "entries_by_service": {
            "payment-service": 1,
            "database-service": 1,
            "api-gateway": 1,
        },
        "earliest_error": (
            "2026-10-09T10:00:02Z ERROR "
            "database-service Connection lost"
        ),
        "supporting_evidence": [
            "2026-10-09T10:00:05Z ERROR payment-service Payment failed",
            "2026-10-09T10:00:02Z ERROR database-service Connection lost",
        ],        
    }


def test_analyse_includes_supporting_log_evidence():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z WARN payment-service Database connection pool at capacity active=20 max=20\n"
        "2026-10-09T10:00:03Z ERROR payment-service Database connection timeout\n"
        "2026-10-09T10:00:04Z ERROR payment-service Payment request failed\n"
        "2026-10-09T10:00:05Z ERROR api-gateway Upstream request failed\n"
    )

    response = client.post(
        "/analyse",
        json={"log_text": logs},
    )

    assert response.status_code == 200

    assert response.json()["supporting_evidence"] == [
        "2026-10-09T10:00:02Z WARN payment-service Database connection pool at capacity active=20 max=20",
        "2026-10-09T10:00:03Z ERROR payment-service Database connection timeout",
        "2026-10-09T10:00:04Z ERROR payment-service Payment request failed",
        "2026-10-09T10:00:05Z ERROR api-gateway Upstream request failed",
    ]

