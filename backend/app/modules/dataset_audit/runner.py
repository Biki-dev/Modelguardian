from pathlib import Path

import pandas as pd

from app.modules.base import AuditModule
from app.modules.dataset_audit.schema_infer import SchemaInfer
from app.modules.dataset_audit.checks import (
    check_missing_values,
    check_duplicates,
    check_constant_columns,
    check_high_cardinality,
    check_outliers,
    check_label_imbalance,
)

from app.schemas.module_output import ModuleOutput, Finding


class DatasetAuditRunner(AuditModule):

    def __init__(self):
        self.schema_infer = SchemaInfer()

    def run(
        self,
        file_path: str,
        target_column: str | None = None,
    ) -> ModuleOutput:

        # --------------------------------------------------
        # Step 1 : Load Dataset
        # --------------------------------------------------

        dataframe = pd.read_csv(file_path)

        # --------------------------------------------------
        # Step 2 : Infer Schema
        # --------------------------------------------------

        schema = self.schema_infer.infer(
            dataframe=dataframe,
            target_column=target_column,
        )

        # --------------------------------------------------
        # Step 3 : Run Checks
        # --------------------------------------------------

        findings: list[Finding] = []

        findings.extend(check_missing_values(dataframe))

        findings.extend(check_duplicates(dataframe))

        findings.extend(check_constant_columns(dataframe))

        findings.extend(check_high_cardinality(dataframe))

        findings.extend(check_outliers(dataframe))

        findings.extend(
            check_label_imbalance(
                dataframe,
                target_column,
            )
        )

        # --------------------------------------------------
        # Step 4 : Score
        # --------------------------------------------------

        score = self._calculate_score(findings)

        severity = self._calculate_severity(findings)

        # --------------------------------------------------
        # Step 5 : Return Contract
        # --------------------------------------------------

        return ModuleOutput(
            module="dataset_audit",
            status="success",
            score=score,
            severity=severity,
            findings=findings,
            artifacts=[],
            summary=(
                f"Dataset contains "
                f"{schema.rows} rows and "
                f"{schema.columns} columns."
            ),
        )

    # ------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------

    def _calculate_score(
        self,
        findings: list[Finding],
    ) -> int:

        score = 100

        for finding in findings:

            if finding.severity == "high":
                score -= 15

            elif finding.severity == "medium":
                score -= 8

            else:
                score -= 3

        return max(score, 0)

    def _calculate_severity(
        self,
        findings: list[Finding],
    ) -> str:

        if any(f.severity == "high" for f in findings):
            return "high"

        if any(f.severity == "medium" for f in findings):
            return "medium"

        return "low"