
DATABASE_POOL_EXHAUSTION_LOGS = """\
2026-10-09T10:00:01Z INFO payment-service Request received request_id=req-101
2026-10-09T10:00:02Z INFO payment-service Acquiring database connection request_id=req-101
2026-10-09T10:00:03Z WARN payment-service Database connection pool at capacity active=20 max=20
2026-10-09T10:00:04Z ERROR payment-service Database connection timeout request_id=req-102
2026-10-09T10:00:05Z ERROR payment-service Payment request failed request_id=req-102
2026-10-09T10:00:06Z ERROR api-gateway Upstream request failed request_id=req-102
"""
