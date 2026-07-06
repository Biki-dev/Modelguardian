from typing import Literal, Any
from pydantic import BaseModel, Field


class Finding(BaseModel):
    title: str
    description: str
    evidence: dict[str, Any] = Field(default_factory=dict)
    recommendation: str
    severity: Literal["low", "medium", "high"] = "low"


class ModuleOutput(BaseModel):
    module: str
    status: Literal["success", "error"]
    score: int = Field(ge=0, le=100)
    severity: Literal["low", "medium", "high"]
    findings: list[Finding] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    summary: str = ""