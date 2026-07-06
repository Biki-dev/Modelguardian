from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Text


class AuditRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    module_name: str
    status: str = "success"
    score: int = 0
    severity: str = "low"
    result_json: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)