from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlmodel import Session

from app.core.db import get_session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead
from app.storage.files import save_upload_file

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectRead)
def create_project(payload: ProjectCreate, session: Session = Depends(get_session)):
    project = Project(
        name=payload.name,
        description=payload.description or "",
        target_column=payload.target_column,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.post("/{project_id}/upload")
def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    project = session.get(Project, project_id)
    if not project:
        return {"error": "Project not found"}

    saved_path = save_upload_file(project_id, file)
    return {
        "project_id": project_id,
        "filename": file.filename,
        "saved_path": saved_path,
    }