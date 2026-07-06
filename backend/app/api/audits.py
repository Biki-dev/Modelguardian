import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.core.config import UPLOAD_DIR

from app.models.project import Project
from app.models.audit_run import AuditRun

from app.modules.dataset_audit.runner import DatasetAuditRunner
from app.modules.leakage.runner import LeakageRunner
from app.storage.files import get_dataset_path

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
)


@router.post("/dataset/{project_id}")
def run_dataset_audit(
    project_id: int,
    session: Session = Depends(get_session),
):

    # -----------------------------------------
    # Check project exists
    # -----------------------------------------

    project = session.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    # -----------------------------------------
    # Find uploaded csv
    # -----------------------------------------

    dataset_path = get_dataset_path(project_id)

    # -----------------------------------------
    # Run audit
    # -----------------------------------------

    runner = DatasetAuditRunner()

    result = runner.run(
        file_path=str(dataset_path),
        target_column=project.target_column,
    )

    # -----------------------------------------
    # Save audit result
    # -----------------------------------------

    audit = AuditRun(
        project_id=project.id,
        module_name="dataset_audit",
        status=result.status,
        score=result.score,
        severity=result.severity,
        result_json=result.model_dump_json(),
    )

    session.add(audit)
    session.commit()

    # -----------------------------------------
    # Return response
    # -----------------------------------------

    return result

@router.post("/leakage/{project_id}")
def run_leakage_audit(
    project_id: int,
    session: Session = Depends(get_session),
):
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.target_column:
        raise HTTPException(
            status_code=400,
            detail="Leakage audit requires a target_column to be set on the project",
        )

    dataset_path = get_dataset_path(project_id)

    runner = LeakageRunner()
    result = runner.run(
        file_path=str(dataset_path),
        target_column=project.target_column,
    )

    audit = AuditRun(
        project_id=project.id,
        module_name="leakage",
        status=result.status,
        score=result.score,
        severity=result.severity,
        result_json=result.model_dump_json(),
    )

    session.add(audit)
    session.commit()

    return result