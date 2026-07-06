import pandas as pd
from app.modules.leakage.runner import LeakageRunner

def run_tests():
    runner = LeakageRunner()
    
    # 1. Clean synthetic data
    df_clean = pd.DataFrame({
        'target': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        'feature1': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        'feature2': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A']
    })
    df_clean.to_csv('test_leakage_clean.csv', index=False)
    
    res1 = runner.run('test_leakage_clean.csv', 'target')
    print("Test 1 (Clean Data):", res1.status)
    assert res1.status == "success"
    assert len(res1.findings) == 0, f"Expected 0 findings, got {len(res1.findings)}"
    
    # 2. Data with leakage
    df_leakage = pd.DataFrame({
        'target': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        'target_leak': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], # Suspicious name and perfect predictor
        'perfect_predictor': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], # Near perfect predictor
        'updated_at': pd.date_range('2023-01-01', periods=10).astype(str) # Datetime leakage
    })
    df_leakage.to_csv('test_leakage_dirty.csv', index=False)
    
    res2 = runner.run('test_leakage_dirty.csv', 'target')
    print("Test 2 (Leakage Data):", res2.status)
    assert res2.status == "success"
    assert len(res2.findings) > 0, "Expected findings due to deliberate leakage"
    
    finding_titles = [f.title for f in res2.findings]
    assert any("Suspiciously named column" in t for t in finding_titles)
    assert any("Potential leakage in" in t for t in finding_titles)

    print("All leakage tests passed!")

if __name__ == "__main__":
    run_tests()
