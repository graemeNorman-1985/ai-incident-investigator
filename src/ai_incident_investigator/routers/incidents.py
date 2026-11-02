
from fastapi import APIRouter, HTTPException
from openai import APIError, APITimeoutError
from fastapi.responses import JSONResponse
from ai_incident_investigator.models.errors import ErrorResponse

from ai_incident_investigator.models.ai_investigation import (
    AIInvestigationReport,
)
from ai_incident_investigator.services.ai_investigation import (
    InvalidEvidenceError,
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

def error_response(
    status_code: int,
    error_code: str,
    detail: str,
) -> JSONResponse:
    """Create a standardised API error response."""
    body = ErrorResponse(
        error_code=error_code,
        detail=detail,
    )

    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(),
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
    responses={
        502: {
            "model": ErrorResponse,
            "description": (
                "The AI investigation failed or returned a report "
                "that did not meet validation requirements."
            ),
        },
        504: {
            "model": ErrorResponse,
            "description": "The AI provider request timed out.",
        },
    },    
)
def analyse_incident_with_ai(
    request: IncidentAnalysisRequest,
) -> AIInvestigationReport | JSONResponse:
    try:
        return investigate_incident(request.log_text)

    # Your current router catches RuntimeError and turns it into HTTP 502. Because InvalidEvidenceError inherits directly from Exception, 
    # the existing RuntimeError handler won't catch it, so we need to add an explicit handler.
    except InvalidEvidenceError as exc:
        return error_response(
            status_code=502,
            error_code="INVALID_AI_EVIDENCE",
            detail="The AI investigation returned invalid supporting evidence.",
        )

    except APITimeoutError as exc:
        return error_response(
            status_code=504,
            error_code="AI_PROVIDER_TIMEOUT",
            detail="The AI investigation request timed out.",
        )

    except APIError as exc:
        return error_response(
            status_code=502,
            error_code="AI_PROVIDER_ERROR",
            detail="The AI investigation provider request failed.",
        )

    except RuntimeError as exc:
        return error_response(
            status_code=502,
            error_code="AI_REPORT_UNAVAILABLE",
            detail="The AI investigation service returned no usable report.",
        )
