"""
This is our ground-truth record. It describes what we intended the scenario to represent.

For this initial exercise, the root cause is the known answer, but our three analysis 
functions don't actually diagnose it yet. They only extract facts from the logs.
"""

DATABASE_POOL_EXHAUSTION_GROUND_TRUTH = {
    "incident_id": "database-pool-exhaustion-001",
    "root_cause": (
        "The database connection pool reached its configured "
        "maximum capacity, leaving new requests unable to "
        "acquire a connection before timing out."
    ),
    "supporting_evidence": [
        "Database connection pool at capacity active=20 max=20",
        "Database connection timeout",
        "Payment request failed",
        "Upstream request failed",
    ],
    "expected_impact": (
        "Some payment requests fail because database operations "
        "cannot obtain connections in time."
    ),
}
