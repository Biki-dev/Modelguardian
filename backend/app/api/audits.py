import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.core.config import UPLOAD_DIR

from app.models.project import Project
from app.models.audit_run import AuditRun

from app.modules.dataset_audit.runner import DatasetAuditRunner

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

    project_folder = UPLOAD_DIR / f"project_{project_id}"

    if not project_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="No uploaded dataset found",
        )

    csv_files = list(project_folder.glob("*.csv"))

    if len(csv_files) == 0:
        raise HTTPException(
            status_code=404,
            detail="CSV dataset not found",
        )

    dataset_path = csv_files[0]

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