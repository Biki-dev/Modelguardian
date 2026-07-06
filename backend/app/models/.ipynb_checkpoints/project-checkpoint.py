from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    target_column: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)