
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response returned by the API."""

    error_code: str = Field(
        description="A stable, machine-readable error identifier."
    )
    detail: str = Field(
        description="A human-readable explanation of the error."
    )
