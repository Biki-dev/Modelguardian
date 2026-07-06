import pandas as pd
from app.schemas.module_output import Finding

def compute_group_gap(df: pd.DataFrame, sensitive_column: str, metric_fn) -> tuple[float, dict]:
    group_scores = df.groupby(sensitive_column).apply(metric_fn)
    return group_scores.max() - group_scores.min(), group_scores.to_dict()

def check_subgroup_accuracy_gap(df: pd.DataFrame, target_column: str, prediction_column: str, sensitive_column: str) -> Finding | None:
    def accuracy(group):
        if len(group) == 0: return 0.0
        return (group[target_column] == group[prediction_column]).mean()
        
    gap, group_scores = compute_group_gap(df, sensitive_column, accuracy)
    
    if gap > 0.1:
        return Finding(
            title="Subgroup Performance Gap",
            description=f"There is a {gap:.1%} gap in accuracy across groups in {sensitive_column}.",
            evidence={"gap": gap, "group_accuracies": group_scores},
            recommendation="Analyze misclassified examples in the underperforming subgroup to identify missing features or underrepresentation.",
            severity="high" if gap > 0.2 else "medium"
        )
    return None

def check_selection_rate_gap(df: pd.DataFrame, prediction_column: str, sensitive_column: str) -> Finding | None:
    def selection_rate(group):
        if len(group) == 0: return 0.0
        return group[prediction_column].mean()
        
    gap, group_scores = compute_group_gap(df, sensitive_column, selection_rate)
    
    if gap > 0.1:
        return Finding(
            title="Selection Rate Gap",
            description=f"There is a {gap:.1%} gap in positive prediction rate across groups in {sensitive_column}.",
            evidence={"gap": gap, "group_selection_rates": group_scores},
            recommendation="Check if the model is overly predicting the negative class for certain groups.",
            severity="high" if gap > 0.2 else "medium"
        )
    return None

def check_fpr_gap(df: pd.DataFrame, target_column: str, prediction_column: str, sensitive_column: str) -> Finding | None:
    def fpr(group):
        negatives = group[group[target_column] == 0]
        if len(negatives) == 0: return 0.0
        return (negatives[prediction_column] == 1).mean()
        
    gap, group_scores = compute_group_gap(df, sensitive_column, fpr)
    
    if gap > 0.1:
        return Finding(
            title="False Positive Rate Gap",
            description=f"There is a {gap:.1%} gap in False Positive Rate across groups in {sensitive_column}.",
            evidence={"gap": gap, "group_fprs": group_scores},
            recommendation="Investigate why certain groups are disproportionately misclassified as positive when they shouldn't be.",
            severity="high" if gap > 0.2 else "medium"
        )
    return None

def check_fnr_gap(df: pd.DataFrame, target_column: str, prediction_column: str, sensitive_column: str) -> Finding | None:
    def fnr(group):
        positives = group[group[target_column] == 1]
        if len(positives) == 0: return 0.0
        return (positives[prediction_column] == 0).mean()
        
    gap, group_scores = compute_group_gap(df, sensitive_column, fnr)
    
    if gap > 0.1:
        return Finding(
            title="False Negative Rate Gap",
            description=f"There is a {gap:.1%} gap in False Negative Rate across groups in {sensitive_column}.",
            evidence={"gap": gap, "group_fnrs": group_scores},
            recommendation="Investigate why certain groups are disproportionately misclassified as negative when they should be positive.",
            severity="high" if gap > 0.2 else "medium"
        )
    return None
