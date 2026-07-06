import pandas as pd

from app.schemas.module_output import Finding


# ---------------------------------------------
# Missing Values
# ---------------------------------------------

def check_missing_values(df: pd.DataFrame) -> list[Finding]:

    findings = []

    missing = df.isnull().sum()

    for column, count in missing.items():

        if count == 0:
            continue

        percent = round((count / len(df)) * 100, 2)

        severity = "low"

        if percent > 30:
            severity = "high"
        elif percent > 10:
            severity = "medium"

        findings.append(
            Finding(
                title=f"Missing values in '{column}'",
                description=f"{count} values are missing.",
                evidence={
                    "column": column,
                    "missing_count": int(count),
                    "missing_percent": percent,
                },
                recommendation="Consider imputing or removing missing values.",
                severity=severity,
            )
        )

    return findings


# ---------------------------------------------
# Duplicate Rows
# ---------------------------------------------

def check_duplicates(df: pd.DataFrame) -> list[Finding]:

    findings = []

    duplicates = int(df.duplicated().sum())

    if duplicates == 0:
        return findings

    findings.append(
        Finding(
            title="Duplicate rows detected",
            description=f"{duplicates} duplicated rows found.",
            evidence={
                "duplicate_rows": duplicates
            },
            recommendation="Remove duplicate records before training.",
            severity="medium",
        )
    )

    return findings


# ---------------------------------------------
# Constant Columns
# ---------------------------------------------

def check_constant_columns(df: pd.DataFrame) -> list[Finding]:

    findings = []

    for column in df.columns:

        if df[column].nunique(dropna=False) == 1:

            findings.append(
                Finding(
                    title=f"Constant column '{column}'",
                    description="Column contains only one unique value.",
                    evidence={
                        "column": column
                    },
                    recommendation="Remove this feature.",
                    severity="low",
                )
            )

    return findings


# ---------------------------------------------
# High Cardinality
# ---------------------------------------------

def check_high_cardinality(df: pd.DataFrame) -> list[Finding]:

    findings = []

    categorical = df.select_dtypes(
        include=["object", "category"]
    )

    for column in categorical.columns:

        unique = df[column].nunique()

        ratio = unique / len(df)

        if ratio > 0.5:

            findings.append(
                Finding(
                    title=f"High Cardinality '{column}'",
                    description=f"{unique} unique values.",
                    evidence={
                        "column": column,
                        "unique_values": unique,
                        "ratio": round(ratio, 2),
                    },
                    recommendation="Consider encoding or grouping categories.",
                    severity="medium",
                )
            )

    return findings


# ---------------------------------------------
# Outliers
# ---------------------------------------------

def check_outliers(df: pd.DataFrame) -> list[Finding]:

    findings = []

    numeric = df.select_dtypes(include=["number"])

    for column in numeric.columns:

        q1 = numeric[column].quantile(0.25)
        q3 = numeric[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = ((numeric[column] < lower) |
                    (numeric[column] > upper)).sum()

        if outliers == 0:
            continue

        findings.append(
            Finding(
                title=f"Outliers in '{column}'",
                description=f"{outliers} possible outliers detected.",
                evidence={
                    "column": column,
                    "outliers": int(outliers),
                },
                recommendation="Review distribution or cap extreme values.",
                severity="medium",
            )
        )

    return findings


# ---------------------------------------------
# Label Imbalance
# ---------------------------------------------

def check_label_imbalance(
    df: pd.DataFrame,
    target_column: str | None,
) -> list[Finding]:

    findings = []

    if target_column is None:
        return findings

    if target_column not in df.columns:
        return findings

    distribution = (
        df[target_column]
        .value_counts(normalize=True)
        .to_dict()
    )
    distribution = {str(k): v for k, v in distribution.items()}

    smallest = min(distribution.values())

    if smallest < 0.10:

        findings.append(
            Finding(
                title="Class imbalance detected",
                description="Target distribution is highly imbalanced.",
                evidence=distribution,
                recommendation="Consider resampling or class weighting.",
                severity="high",
            )
        )

    return findings