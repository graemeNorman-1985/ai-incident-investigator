from pydantic import BaseModel, Field

class IncidentAnalysisRequest(BaseModel):
    log_text: str = Field(min_length=1)


class IncidentAnalysisResponse(BaseModel):
    summary: str
    error_count: int
    entries_by_service: dict[str, int]
    earliest_error: str | None
    supporting_evidence: list[str]
