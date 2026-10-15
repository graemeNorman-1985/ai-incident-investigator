
from ai_incident_investigator.services.log_analysis import (
    count_error_entries,
    group_logs_by_service,
    find_earliest_error,
    extract_supporting_evidence,
)


# Tests for count_error_entries FUNCTION

def test_mixed_error_and_info_entries():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "2026-10-09T10:00:03Z ERROR payment-service Payment request failed\n"
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed\n"
        "2026-10-09T10:00:05Z INFO api-gateway Request completed"
    )

    assert count_error_entries(logs) == 3


def test_only_info_entries():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:05Z INFO api-gateway Request completed"
    )

    assert count_error_entries(logs) == 0


def test_count_error_entries_empty_string():
    assert count_error_entries("") == 0




# TESTS FOR group_logs_by_service FUNCTION

def test_five_entries_two_services():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "2026-10-09T10:00:03Z ERROR payment-service Payment request failed\n"
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed\n"
        "2026-10-09T10:00:05Z INFO api-gateway Request completed"
    )

    assert group_logs_by_service(logs) == {
        "payment-service": 3,
        "api-gateway": 2,
    }


def test_entries_from_one_service():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "2026-10-09T10:00:03Z ERROR payment-service Payment request failed"
    )

    assert group_logs_by_service(logs) == {
        "payment-service": 3,
    }

def test_entries_malformed_entry():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "this is not a valid log entry\n"
        "2026-10-09T10:00:03Z ERROR payment-service Payment request failed"
    )

    assert group_logs_by_service(logs) == {
        "payment-service": 3,
    }

def test_group_logs_by_service_empty_string():
    assert group_logs_by_service("") == {}


# TESTS FOR find_earliest_error FUNCTION


def test_five_entries_output_earliest_error():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "2026-10-09T10:00:03Z ERROR payment-service Payment request failed\n"
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed\n"
        "2026-10-09T10:00:05Z INFO api-gateway Request completed"
    )

    assert find_earliest_error(logs) == "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout"


def test_find_earliest_error_returns_none_when_no_errors():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z INFO payment-service Database connection timeout\n"
    )

    assert find_earliest_error(logs) == None

def test_find_earliest_error_skips_malformed_line_before_valid_error():
    logs = (
        "this is not a valid error log entry\n"
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:03Z INFO payment-service Payment request failed\n"
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed\n"
        "2026-10-09T10:00:05Z INFO api-gateway Request completed"
    )

    assert find_earliest_error(logs) == "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed"

def test_find_earliest_error_handles_out_of_order_timestamps():
    logs = (
        "2026-10-09T10:00:05Z ERROR payment-service Payment failed\n"
        "2026-10-09T10:00:02Z ERROR database-service Connection lost\n"
        "2026-10-09T10:00:03Z INFO api-gateway Request received"
    )

    assert find_earliest_error(logs) == (
        "2026-10-09T10:00:02Z ERROR database-service Connection lost"
    )

def test_find_earliest_error_skips_invalid_timestamp():
    logs = (
        "not-a-timestamp ERROR payment-service Cannot parse timestamp\n"
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed"
    )

    assert find_earliest_error(logs) == (
        "2026-10-09T10:00:04Z ERROR api-gateway Upstream request failed"
    )    

def test_count_error_entries_skips_malformed_lines():
    logs = (
        "not-a-valid-entry ERROR\n"
        "2026-10-09T10:00:02Z ERROR payment-service Database connection timeout\n"
        "this is not a valid log entry"
    )

    assert count_error_entries(logs) == 1


def test_extract_supporting_evidence_includes_warnings_and_errors():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z WARN payment-service Connection pool at capacity\n"
        "2026-10-09T10:00:03Z ERROR payment-service Database timeout\n"
    )

    assert extract_supporting_evidence(logs) == [
        "2026-10-09T10:00:02Z WARN payment-service Connection pool at capacity",
        "2026-10-09T10:00:03Z ERROR payment-service Database timeout",
    ]


def test_extract_supporting_evidence_returns_empty_list_without_warnings_or_errors():
    logs = (
        "2026-10-09T10:00:01Z INFO payment-service Request received\n"
        "2026-10-09T10:00:02Z INFO api-gateway Request completed"
    )

    assert extract_supporting_evidence(logs) == []
