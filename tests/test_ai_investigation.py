
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_incident_investigator.models.ai_investigation import (
    AIInvestigationReport,
)
from ai_incident_investigator.services.ai_investigation import (
    investigate_incident,
)


def make_investigation_report() -> AIInvestigationReport:
    """Create a predictable report for use in tests."""
    return AIInvestigationReport(
        summary="The payment service experienced database timeouts.",
        likely_root_cause=(
            "Database connection pool exhaustion is a plausible cause."
        ),
        supporting_evidence=[
            "2026-10-09T10:00:04Z ERROR payment-service Database timeout"
        ],
        alternative_hypotheses=["The database may be responding slowly."],
        recommended_next_steps=[
            "Inspect database connection pool metrics."
        ],
        uncertainties=[
            "Database-side logs and metrics were not supplied."
        ],
    )


def test_investigate_incident_returns_parsed_report():
    logs = (
        "2026-10-09T10:00:04Z ERROR payment-service Database timeout"
    )
    expected_report = make_investigation_report()

    mock_client = MagicMock()
    mock_client.responses.parse.return_value = SimpleNamespace(
        output_parsed=expected_report
    )

    report = investigate_incident(logs, client=mock_client)

    assert report == expected_report

    mock_client.responses.parse.assert_called_once()

    call_kwargs = mock_client.responses.parse.call_args.kwargs

    assert call_kwargs["text_format"] is AIInvestigationReport
    assert logs in call_kwargs["input"]


def test_investigate_incident_raises_when_no_parsed_report():
    mock_client = MagicMock()
    mock_client.responses.parse.return_value = SimpleNamespace(
        output_parsed=None
    )

    with pytest.raises(
        RuntimeError,
        match="did not return a parsed investigation report",
    ):
        investigate_incident(
            "2026-10-09T10:00:04Z ERROR payment-service Database timeout",
            client=mock_client,
        )
