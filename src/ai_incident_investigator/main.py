from fastapi import FastAPI

from ai_incident_investigator.routers import incidents

app = FastAPI(title="AI Incident Investigator")

app.include_router(incidents.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}