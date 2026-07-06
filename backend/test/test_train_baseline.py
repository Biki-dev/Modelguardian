import pandas as pd
import pytest
from app.modules.common.baseline_model import train_baseline
from sklearn.pipeline import Pipeline

def test_train_baseline_classification():
    # Small synthetic classification frame
    df = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "feature2": ["A", "A", "A", "B", "B", "C", "C", "C", "C", "C"],
        "target": [0, 0, 0, 1, 1, 1, 1, 0, 1, 0]
    })
    
    model, task_type = train_baseline(df, "target")
    
    assert isinstance(model, Pipeline)
    assert task_type == "classification"
    
    # Check that model can predict
    preds = model.predict(df.drop(columns=["target"]))
    assert len(preds) == 10

def test_train_baseline_regression():
    # Small synthetic regression frame
    df = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "target": [1.1, 2.0, 3.2, 4.0, 5.1, 6.0, 7.3, 8.0, 9.1, 10.0]
    })
    
    model, task_type = train_baseline(df, "target")
    
    assert isinstance(model, Pipeline)
    assert task_type == "regression"
    
def test_train_baseline_missing_target():
    df = pd.DataFrame({
        "feature1": [1, 2, 3],
        "target": [None, None, None]
    })
    
    with pytest.raises(ValueError, match="No valid rows remaining"):
        train_baseline(df, "target")
