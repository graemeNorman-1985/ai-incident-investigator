
from fastapi import APIRouter, HTTPException
from openai import APIError, APITimeoutError

from ai_incident_investigator.models.ai_investigation import (
    AIInvestigationReport,
)
from ai_incident_investigator.services.ai_investigation import (
    investigate_incident,
)

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


@router.post(
    "/analyse/ai",
    response_model=AIInvestigationReport,
)
def analyse_incident_with_ai(
    request: IncidentAnalysisRequest,
) -> AIInvestigationReport:
    try:
        return investigate_incident(request.log_text)

    except APITimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI investigation request timed out.",
        ) from exc

    except APIError as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI investigation provider request failed.",
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI investigation service returned no usable report.",
        ) from exc

