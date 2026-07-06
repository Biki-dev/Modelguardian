import pandas as pd
import numpy as np
from typing import List, Dict, Any

def compute_local_explanation(model_pipeline: Any, X: pd.DataFrame, sample_row_index: int, task_type: str) -> List[Dict[str, Any]]:
    """
    Computes a simple local explanation for a single row by measuring the 
    prediction change when each feature is replaced by its dataset baseline (mean/mode).
    """
    if sample_row_index < 0 or sample_row_index >= len(X):
        raise IndexError(f"sample_row_index {sample_row_index} is out of bounds.")
    
    # Extract the row to explain
    row_to_explain = X.iloc[[sample_row_index]].copy()
    
    # Calculate dataset baselines (mean for numeric, mode for categorical)
    baselines = {}
    for col in X.columns:
        if pd.api.types.is_numeric_dtype(X[col]):
            baselines[col] = X[col].mean()
        else:
            baselines[col] = X[col].mode()[0]
            
    # Base prediction for the row
    if task_type == "classification":
        # Predict probability of the positive class (class index 1 if binary)
        # For multi-class, let's just use the predicted class probability
        probs = model_pipeline.predict_proba(row_to_explain)[0]
        pred_class = model_pipeline.predict(row_to_explain)[0]

        if hasattr(pred_class, "item"):
            pred_class = pred_class.item()
        # Find index of predicted class
        class_idx = list(model_pipeline.classes_).index(pred_class)
        base_pred = probs[class_idx]
    else:
        base_pred = model_pipeline.predict(row_to_explain)[0]
        
    contributions = []
    
    # Measure contribution of each feature
    for col in X.columns:
        # Create a modified row where this feature is replaced by its baseline
        modified_row = row_to_explain.copy()
        modified_row[col] = baselines[col]
        
        if task_type == "classification":
            mod_probs = model_pipeline.predict_proba(modified_row)[0]
            mod_pred = mod_probs[class_idx]
        else:
            mod_pred = model_pipeline.predict(modified_row)[0]
            
        # Contribution is how much the ACTUAL value moved the prediction
        # compared to the BASELINE value.
        # If actual value makes prediction 0.8 and baseline makes it 0.5,
        # contribution is +0.3.
        contribution = base_pred - mod_pred
        
        # Get actual value to display
        actual_val = row_to_explain[col].iloc[0]

        # Convert NumPy scalars to native Python types
        if isinstance(actual_val, np.generic):
            actual_val = actual_val.item()

        contributions.append(
        {
          "feature": str(col),
          "actual_value": actual_val,
          "contribution": float(contribution),
        }
    )
        
    # Sort by absolute contribution descending
    contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    
    return contributions
