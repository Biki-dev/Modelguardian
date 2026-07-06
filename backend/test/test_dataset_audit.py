import pandas as pd
from app.modules.dataset_audit.runner import DatasetAuditRunner

def run_tests():
    runner = DatasetAuditRunner()
    
    # 1. Clean synthetic data
    df_clean = pd.DataFrame({
        'target': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    })
    df_clean.to_csv('test_clean.csv', index=False)
    
    res1 = runner.run('test_clean.csv', 'target')
    print("Test 1 (Clean Data):", res1.status)
    assert res1.status == "success"
    assert len(res1.findings) == 0, f"Expected 0 findings, got {len(res1.findings)}"
    
    # 2. Dirty synthetic data
    df_dirty = pd.DataFrame({
        'target': [1]*10 + [0]*1, # Imbalance (1/11 < 0.1)
        'missing_col': [1, None, 3, 4, 5, 6, 7, 8, 9, 10, 11], # Missing values
        'constant_col': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], # Constant
        'high_card_col': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], # High cardinality
    })
    df_dirty.to_csv('test_dirty.csv', index=False)
    
    res2 = runner.run('test_dirty.csv', 'target')
    print("Test 2 (Dirty Data):", res2.status)
    assert res2.status == "success"
    assert len(res2.findings) > 0, "Expected findings due to deliberate issues"
    
    # Verify we got the specific findings
    finding_titles = [f.title for f in res2.findings]
    assert any("Missing values" in t for t in finding_titles)
    assert any("Constant column" in t for t in finding_titles)
    assert any("High Cardinality" in t for t in finding_titles)
    assert any("Class imbalance" in t for t in finding_titles)

    print("All dataset audit tests passed!")

if __name__ == "__main__":
    run_tests()
