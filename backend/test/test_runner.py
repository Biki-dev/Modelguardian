import pandas as pd
from app.modules.explainability.runner import ExplainabilityRunner

def test_explainability_runner_success(tmp_path):
    # Create mock dataset
    df = pd.DataFrame({
        "driver": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "noise": [10, 1, 9, 2, 8, 3, 7, 4, 6, 5],
        "target": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    })
    
    file_path = tmp_path / "data.csv"
    df.to_csv(file_path, index=False)
    
    runner = ExplainabilityRunner()
    result = runner.run(str(file_path), target_column="target", sample_row_index=0)
    
    assert result.status == "success"
    assert result.module == "explainability"
    assert len(result.findings) == 2
    
    global_finding = next(f for f in result.findings if f.title == "Global Feature Importance")
    assert "importance_list" in global_finding.evidence
    
    local_finding = next(f for f in result.findings if f.title.startswith("Local Explanation"))
    assert "contributions" in local_finding.evidence
    assert local_finding.evidence["row_index"] == 0

def test_explainability_runner_out_of_bounds_index(tmp_path):
    df = pd.DataFrame({
        "driver": [1, 2, 3],
        "target": [0, 1, 0]
    })
    
    file_path = tmp_path / "data.csv"
    df.to_csv(file_path, index=False)
    
    runner = ExplainabilityRunner()
    result = runner.run(str(file_path), target_column="target", sample_row_index=10)
    
    assert result.status == "error"
    assert "out of bounds" in result.summary.lower()
