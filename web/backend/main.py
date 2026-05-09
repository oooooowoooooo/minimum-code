"""
minimum-code — AI App Engineer Training System Backend
======================================================
Serves competency tracks, labs, assessment, and interview expression APIs.
This project itself is a FastAPI meta-example: it teaches FastAPI by using FastAPI.

Run: cd web/backend && uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import knowledge, modules, weeks, progress, tracks, labs, assessment, interview
from app.core.config import ALLOWED_ORIGINS, APP_NAME
from app.services import data_service

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    data_service.load_knowledge_points()


# Include all routers
app.include_router(modules.router)
app.include_router(knowledge.router)
app.include_router(weeks.router)
app.include_router(progress.router)
app.include_router(tracks.router)
app.include_router(labs.router)
app.include_router(assessment.router)
app.include_router(interview.router)
