from datetime import datetime, timezone

def count_error_entries(logs: str) -> int:
    """
    Counts the number of log entries with the log level 'ERROR'.
    
    Args:
        logs: A multiline string containing log entries formatted as:
              '<timestamp> <level> <service> <message>'
              
    Returns:
        int: Total number of log entries with level 'ERROR'.
    """
    count = 0
    for line in logs.splitlines():
        parts = line.split()
        # we check part 4 because the expected log structure is: timestamp, level, service, message. 
        # If there are fewer than 4 parts, it's malformed.
        if len(parts) >= 4 and parts[1] == "ERROR":
            count += 1
    return count


########################################################################################################################


VALID_LOG_LEVELS = {"INFO", "ERROR", "WARN"} # , "WARNING", "DEBUG", "TRACE", "FATAL", "CRITICAL" types coming later

def group_logs_by_service(logs: str) -> dict[str, int]:
    """
    Counts the number of log entries for each service.
    Skips malformed or invalid log lines.
    
    Args:
        logs: A multiline string containing log entries formatted as:
              '<timestamp> <level> <service> <message>'
              
    Returns:
        dict: A dictionary where keys are service names and values are total entry counts.
    """
    service_counts = {}
    for line in logs.splitlines():
        parts = line.split()
        
        # Validate that the line has required fields and a recognised log level
        if len(parts) >= 3 and parts[1] in VALID_LOG_LEVELS:
            service = parts[2]
            service_counts[service] = service_counts.get(service, 0) + 1
            
    return service_counts



def find_earliest_error(logs: str) -> str | None:
    """
    Finds the earliest ERROR log entry by timestamp.

    Returns:
        The earliest ERROR log entry, or None if no valid
        ERROR entries are found.
    """
    earliest_timestamp: datetime | None = None
    earliest_error: str | None = None

    for line in logs.splitlines():
        parts = line.split()

        # Skip lines that don't match the expected log structure.
        if len(parts) < 4 or parts[1] != "ERROR":
            continue

        # Parse the timestamp, skipping entries with invalid timestamps.
        try:
            timestamp = datetime.fromisoformat(
                parts[0].replace("Z", "+00:00")
            )
        except ValueError:
            continue

        # Treat timestamps without a timezone as UTC.
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        # Keep the error with the earliest timestamp.
        if (earliest_timestamp is None or timestamp < earliest_timestamp):
            earliest_timestamp = timestamp
            earliest_error = line

    return earliest_error



def extract_supporting_evidence(logs: str) -> list[str]:
    """
    Returns valid warning and error log entries as supporting evidence.
    """
    supporting_evidence = []

    for line in logs.splitlines():
        parts = line.split()

        if (
            len(parts) >= 4
            and parts[1] in VALID_LOG_LEVELS
            and parts[1] in {"WARN", "ERROR"}
        ):
            supporting_evidence.append(line)

    return supporting_evidence
