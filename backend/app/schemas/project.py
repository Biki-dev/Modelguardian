from typing import Optional
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    target_column: Optional[str] = None


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str = ""
    target_column: Optional[str] = None

    class Config:
        from_attributes = True