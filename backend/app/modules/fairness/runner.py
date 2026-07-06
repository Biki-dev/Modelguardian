import pandas as pd
from app.schemas.module_output import ModuleOutput, Finding
from app.modules.fairness.checks import (
    check_subgroup_accuracy_gap,
    check_selection_rate_gap,
    check_fpr_gap,
    check_fnr_gap,
)

class FairnessRunner:
    def run(self, file_path: str, target_column: str, prediction_column: str, sensitive_column: str) -> ModuleOutput:
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return ModuleOutput(
                module="fairness",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Failed to read dataset: {str(e)}"
            )

        if target_column not in df.columns:
            return ModuleOutput(
                module="fairness",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Target column '{target_column}' not found in dataset."
            )

        if prediction_column not in df.columns:
            return ModuleOutput(
                module="fairness",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Prediction column '{prediction_column}' not found in dataset."
            )
            
        if sensitive_column not in df.columns:
            return ModuleOutput(
                module="fairness",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Sensitive column '{sensitive_column}' not found in dataset."
            )

        # Basic binary check for target and prediction (for MVP)
        if not set(df[target_column].dropna().unique()).issubset({0, 1, 0.0, 1.0}):
            return ModuleOutput(
                module="fairness",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Target column '{target_column}' must be binary (0/1) for fairness audit."
            )
            
        if not set(df[prediction_column].dropna().unique()).issubset({0, 1, 0.0, 1.0}):
            return ModuleOutput(
                module="fairness",
                status="error",
                score=0,
                severity="high",
                findings=[],
                summary=f"Prediction column '{prediction_column}' must be binary (0/1) for fairness audit."
            )

        df = df.dropna(subset=[target_column, prediction_column, sensitive_column])
        
        findings = []
        
        f1 = check_subgroup_accuracy_gap(df, target_column, prediction_column, sensitive_column)
        if f1: findings.append(f1)
        
        f2 = check_selection_rate_gap(df, prediction_column, sensitive_column)
        if f2: findings.append(f2)
        
        f3 = check_fpr_gap(df, target_column, prediction_column, sensitive_column)
        if f3: findings.append(f3)
        
        f4 = check_fnr_gap(df, target_column, prediction_column, sensitive_column)
        if f4: findings.append(f4)

        score = 100
        severity = "low"

        for f in findings:
            if f.severity == "high":
                score -= 30
            elif f.severity == "medium":
                score -= 15

        score = max(0, score)

        if any(f.severity == "high" for f in findings):
            severity = "high"
        elif any(f.severity == "medium" for f in findings):
            severity = "medium"

        return ModuleOutput(
            module="fairness",
            status="success",
            score=score,
            severity=severity,
            findings=findings,
            summary=f"Fairness audit complete. Found {len(findings)} potential fairness issues."
        )
