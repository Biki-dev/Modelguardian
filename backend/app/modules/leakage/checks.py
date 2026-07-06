import pandas as pd
from app.schemas.module_output import Finding

SUSPICIOUS_KEYWORDS = ["label", "target", "outcome", "result", "final", "actual"]

def check_suspicious_names(df: pd.DataFrame, target_column: str) -> list[Finding]:
    findings = []
    for col in df.columns:
        if col == target_column:
            continue
            
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in SUSPICIOUS_KEYWORDS):
            # Check for high correlation or purity to avoid false positives
            is_suspicious = False
            
            try:
                # If target is categorical or low cardinality
                if df[target_column].dtype == 'object' or df[target_column].nunique() < 20:
                    purity = df.groupby(col)[target_column].apply(
                        lambda g: g.value_counts(normalize=True).max()
                    ).mean()
                    if purity > 0.7:  # Lower threshold for suspiciously named columns
                        is_suspicious = True
                else:
                    # If target is numeric and col is numeric
                    if pd.api.types.is_numeric_dtype(df[col]) and pd.api.types.is_numeric_dtype(df[target_column]):
                        corr = abs(df[col].corr(df[target_column]))
                        if corr > 0.7:
                            is_suspicious = True
            except Exception:
                pass
                
            if is_suspicious:
                findings.append(Finding(
                    title=f"Suspiciously named column '{col}' with high correlation",
                    description=f"Column name contains keyword '{col_lower}' typically used for targets, and correlates strongly with the actual target.",
                    evidence={"column": col},
                    recommendation="Ensure this column is not leaking the target variable.",
                    severity="high",
                ))
    return findings

def check_near_perfect_predictor(df: pd.DataFrame, target_column: str, threshold: float = 0.95) -> list[Finding]:
    findings = []
    for col in df.columns:
        if col == target_column:
            continue
            
        # Check purity for categorical targets
        if df[target_column].dtype == 'object' or str(df[target_column].dtype) == 'category' or df[target_column].nunique() < 20:
            try:
                purity = df.groupby(col)[target_column].apply(
                    lambda g: g.value_counts(normalize=True).max()
                ).mean()
                if purity > threshold:
                    findings.append(Finding(
                        title=f"Potential leakage in '{col}'",
                        description=f"Column almost fully determines the target (purity={purity:.2f}).",
                        evidence={"column": col, "purity": round(purity, 3)},
                        recommendation="Verify this feature isn't derived from the target.",
                        severity="high",
                    ))
            except Exception:
                pass
        else:
            # Check correlation for numeric targets
            if pd.api.types.is_numeric_dtype(df[col]) and pd.api.types.is_numeric_dtype(df[target_column]):
                try:
                    corr = abs(df[col].corr(df[target_column]))
                    if corr > threshold:
                        findings.append(Finding(
                            title=f"Potential leakage in '{col}'",
                            description=f"Column is highly correlated with the target (correlation={corr:.2f}).",
                            evidence={"column": col, "correlation": round(corr, 3)},
                            recommendation="Verify this feature isn't derived from the target.",
                            severity="high",
                        ))
                except Exception:
                    pass
    return findings

def check_datetime_leakage(datetime_columns: list[str]) -> list[Finding]:
    findings = []
    for col in datetime_columns:
        findings.append(Finding(
            title=f"Potential temporal leakage in '{col}'",
            description=f"Datetime columns can accidentally leak future information.",
            evidence={"column": col},
            recommendation="Manually verify that values in this column are known at prediction time.",
            severity="medium",
        ))
    return findings
