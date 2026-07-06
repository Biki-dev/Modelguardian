from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import UPLOAD_DIR


def save_upload_file(project_id: int, file: UploadFile) -> str:
    project_dir = UPLOAD_DIR / f"project_{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)

    file_path = project_dir / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)

def get_dataset_path(project_id: int) -> Path:
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
    
    return csv_files[0]


def load_csv(file_path: str):
    import pandas as pd
    return pd.read_csv(file_path)