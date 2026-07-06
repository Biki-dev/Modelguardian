import pandas as pd
from sklearn.inspection import permutation_importance
from typing import List, Dict, Any

def compute_global_importance(model_pipeline: Any, X: pd.DataFrame, y: pd.Series, random_state: int = 42) -> List[Dict[str, Any]]:
    """
    Computes global feature importance using permutation importance.
    Returns a sorted list of features and their importance scores.
    """
    # Use permutation importance on the original dataframe
    # This automatically handles preprocessing within the pipeline and gives importance
    # for the original columns (before one-hot encoding etc.)
    result = permutation_importance(
        model_pipeline, 
        X, 
        y, 
        n_repeats=5, 
        random_state=random_state, 
        n_jobs=-1
    )
    
    importances = result.importances_mean
    
    # Pair feature names with importance scores
    feature_importance_list = []
    for i, col in enumerate(X.columns):
        feature_importance_list.append({
            "feature": col,
            "importance": float(importances[i])
        })
        
    # Sort by importance descending
    feature_importance_list.sort(key=lambda x: x["importance"], reverse=True)
    
    return feature_importance_list
