import pandas as pd
import pytest
from app.modules.common.baseline_model import train_baseline
from app.modules.explainability.global_importance import compute_global_importance
from app.modules.explainability.local_explanation import compute_local_explanation

@pytest.fixture
def dummy_model_and_data():
    # Construct data where one column obviously drives the target, one is noise
    df = pd.DataFrame({
        "driver": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "noise": [10, 1, 9, 2, 8, 3, 7, 4, 6, 5],
        "target": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    })
    
    model, task_type = train_baseline(df, "target", random_state=42)
    X = df.drop(columns=["target"])
    y = df["target"]
    
    return model, X, y, task_type

def test_global_importance_ranks_relevant_feature_higher(dummy_model_and_data):
    model, X, y, task_type = dummy_model_and_data
    
    importances = compute_global_importance(model, X, y, random_state=42)
    
    assert len(importances) == 2
    # Ensure driver is ranked higher than noise
    assert importances[0]["feature"] == "driver"
    assert importances[1]["feature"] == "noise"

def test_local_explanation_returns_all_features(dummy_model_and_data):
    model, X, y, task_type = dummy_model_and_data
    
    contributions = compute_local_explanation(model, X, sample_row_index=0, task_type=task_type)
    
    assert len(contributions) == 2
    features = [c["feature"] for c in contributions]
    assert "driver" in features
    assert "noise" in features
    
    # Check shape
    for c in contributions:
        assert "feature" in c
        assert "actual_value" in c
        assert "contribution" in c
        assert isinstance(c["contribution"], float)

def test_local_explanation_out_of_bounds(dummy_model_and_data):
    model, X, y, task_type = dummy_model_and_data
    
    with pytest.raises(IndexError):
        compute_local_explanation(model, X, sample_row_index=100, task_type=task_type)
