
from ai_incident_investigator.data.incidents import (
    DATABASE_POOL_EXHAUSTION_LOGS,
)
from ai_incident_investigator.services.ai_investigation import (
    investigate_incident,
)


def main() -> None:
    report = investigate_incident(DATABASE_POOL_EXHAUSTION_LOGS)

    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
