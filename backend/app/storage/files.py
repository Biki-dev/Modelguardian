from pathlib import Path
from fastapi import UploadFile
from app.core.config import UPLOAD_DIR


def save_upload_file(project_id: int, file: UploadFile) -> str:
    project_dir = UPLOAD_DIR / f"project_{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)

    file_path = project_dir / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)


def load_csv(file_path: str):
    import pandas as pd
    return pd.read_csv(file_path)