import pandas as pd
from app.modules.base import AuditModule
from app.modules.dataset_audit.schema_infer import SchemaInfer
from app.modules.leakage.checks import (
    check_suspicious_names,
    check_near_perfect_predictor,
    check_datetime_leakage
)
from app.schemas.module_output import ModuleOutput, Finding

class LeakageRunner(AuditModule):
    def __init__(self):
        self.schema_infer = SchemaInfer()

    def run(self, file_path: str, target_column: str) -> ModuleOutput:
        # Load dataset
        dataframe = pd.read_csv(file_path)

        # Infer schema
        schema = self.schema_infer.infer(
            dataframe=dataframe,
            target_column=target_column,
        )

        findings: list[Finding] = []

        # Run checks
        findings.extend(check_suspicious_names(dataframe, target_column))
        findings.extend(check_near_perfect_predictor(dataframe, target_column))
        
        if schema.datetime_columns:
            findings.extend(check_datetime_leakage(schema.datetime_columns))

        # Calculate score and severity
        score = self._calculate_score(findings)
        severity = self._calculate_severity(findings)

        # Build output
        return ModuleOutput(
            module="leakage",
            status="success",
            score=score,
            severity=severity,
            findings=findings,
            artifacts=[],
            summary=f"Analyzed {schema.columns - 1} features against target '{target_column}' for data leakage.",
        )

    def _calculate_score(self, findings: list[Finding]) -> int:
        score = 100
        for finding in findings:
            if finding.severity == "high":
                score -= 30
            elif finding.severity == "medium":
                score -= 10
            else:
                score -= 5
        return max(score, 0)

    def _calculate_severity(self, findings: list[Finding]) -> str:
        if any(f.severity == "high" for f in findings):
            return "high"
        if any(f.severity == "medium" for f in findings):
            return "medium"
        return "low"
