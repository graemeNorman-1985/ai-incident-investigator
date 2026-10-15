from ai_incident_investigator.data.incidents import (
    DATABASE_POOL_EXHAUSTION_LOGS,
)


def test_database_pool_exhaustion_fixture_contains_six_entries():
    entries = DATABASE_POOL_EXHAUSTION_LOGS.splitlines()

    assert len(entries) == 6


def test_database_pool_exhaustion_fixture_contains_connection_timeout():
    assert "Database connection timeout" in DATABASE_POOL_EXHAUSTION_LOGS
