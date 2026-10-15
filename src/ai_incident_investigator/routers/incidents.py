
from fastapi import APIRouter
from ai_incident_investigator.models.incident import (
    IncidentAnalysisRequest,
    IncidentAnalysisResponse,
)
from ai_incident_investigator.services.log_analysis import (
    count_error_entries,
    group_logs_by_service,
    find_earliest_error,
    extract_supporting_evidence,
)

router = APIRouter()

@router.post(
    "/analyse",
    response_model=IncidentAnalysisResponse,
)
def analyse_incident(
    request: IncidentAnalysisRequest,
) -> IncidentAnalysisResponse:
    logs = request.log_text

    error_count = count_error_entries(logs)
    entries_by_service = group_logs_by_service(logs)
    earliest_error = find_earliest_error(logs)
    supporting_evidence = extract_supporting_evidence(logs)
    summary = (
        f"Found {error_count} error entries "
        f"across {len(entries_by_service)} services."
    )

    return IncidentAnalysisResponse(
        summary=summary,
        error_count=error_count,
        entries_by_service=entries_by_service,
        earliest_error=earliest_error,
        supporting_evidence=supporting_evidence,
    )


