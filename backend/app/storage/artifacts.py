from pathlib import Path
from app.core.config import ARTIFACT_DIR


def get_project_artifact_dir(project_id: int) -> Path:
    project_dir = ARTIFACT_DIR / f"project_{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def save_text_artifact(project_id: int, filename: str, content: str) -> str:
    project_dir = get_project_artifact_dir(project_id)
    path = project_dir / filename
    path.write_text(content, encoding="utf-8")
    return str(path)