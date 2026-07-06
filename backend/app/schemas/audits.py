from pydantic import BaseModel

class FairnessAuditRequest(BaseModel):
    prediction_column: str
    sensitive_column: str

class ExplainabilityAuditRequest(BaseModel):
    sample_row_index: int = 0
