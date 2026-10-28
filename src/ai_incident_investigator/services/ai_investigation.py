
from openai import OpenAI

from ai_incident_investigator.models.ai_investigation import (
    AIInvestigationReport,
)


MODEL = "gpt-5-mini"

INVESTIGATION_INSTRUCTIONS = (
    "You are an experienced software incident investigator. "
    "Analyse the supplied application logs and produce a careful, "
    "evidence-based investigation report. Distinguish observed facts "
    "from hypotheses. Do not claim that a root cause is confirmed "
    "unless the logs establish it. Every supporting evidence item "
    "must be an exact log line copied from the supplied logs. "
    "Do not invent evidence or details that are not present."
)


def investigate_incident(
    logs: str,
    client: OpenAI | None = None,
) -> AIInvestigationReport:
    """Generate a structured AI investigation report from application logs."""
    openai_client = client if client is not None else OpenAI()

    response = openai_client.responses.parse(
        model=MODEL,
        instructions=INVESTIGATION_INSTRUCTIONS,
        input=(
            "Investigate this application incident using the following "
            "log bundle:\n\n"
            f"{logs}"
        ),
        text_format=AIInvestigationReport,
    )

    report = response.output_parsed

    if report is None:
        raise RuntimeError(
            "OpenAI did not return a parsed investigation report."
        )

    return report
