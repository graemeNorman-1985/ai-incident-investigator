
from openai import OpenAI

from ai_incident_investigator.data.incidents import (
    DATABASE_POOL_EXHAUSTION_LOGS,
)
from ai_incident_investigator.models.ai_investigation import (
    AIInvestigationReport,
)


def main() -> None:
    client = OpenAI()

    response = client.responses.parse(
        model="gpt-5-mini",
        instructions=(
            "You are an experienced software incident investigator. "
            "Analyse the supplied application logs and produce a "
            "careful, evidence-based investigation report. "
            "Distinguish observed facts from hypotheses. "
            "Do not claim that a root cause is confirmed unless the "
            "logs establish it. Every supporting evidence item must "
            "be an exact log line copied from the supplied logs. "
            "Do not invent evidence or details that are not present."
        ),
        input=(
            "Investigate this application incident using the following "
            "log bundle:\n\n"
            f"{DATABASE_POOL_EXHAUSTION_LOGS}"
        ),
        text_format=AIInvestigationReport,
    )

    report = response.output_parsed

    if report is None:
        raise RuntimeError(
            "The API response did not contain a parsed investigation report."
        )

    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
