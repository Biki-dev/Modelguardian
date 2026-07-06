from pydantic import BaseModel

class FairnessAuditRequest(BaseModel):
    prediction_column: str
    sensitive_column: str
