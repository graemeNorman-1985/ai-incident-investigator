from pydantic import BaseModel, Field

# Think of this as a structured summary of the investigation findings, which can be used to communicate the results to engineers or other stakeholders.
# Essentially a contract between the AI and our application.

class AIInvestigationReport(BaseModel):
    summary: str = Field(
        description="A concise summary of the incident and its symptoms."
    )

    likely_root_cause: str = Field(
        description=(
            "The most plausible explanation supported by the evidence. "
            "Distinguish a hypothesis from a confirmed root cause."
        )
    )

    supporting_evidence: list[str] = Field(
        description=(
            "Specific log entries from the supplied logs that support "
            "the investigation findings."
        )
    )

    alternative_hypotheses: list[str] = Field(
        description=(
            "Other plausible explanations worth considering. "
            "Use an empty list if there are none worth mentioning."
        )
    )

    recommended_next_steps: list[str] = Field(
        description="Practical steps an engineer should take to investigate."
    )

    uncertainties: list[str] = Field(
        description=(
            "Missing information, unresolved questions, or limitations "
            "that prevent a confident conclusion."
        )
    )
