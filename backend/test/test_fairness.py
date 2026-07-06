import pandas as pd
from app.modules.fairness.runner import FairnessRunner
from app.schemas.module_output import ModuleOutput

def run_tests():
    runner = FairnessRunner()
    
    # 1. Perfectly fair synthetic data (equal rates across groups)
    df_fair = pd.DataFrame({
        'target': [1, 1, 0, 0, 1, 1, 0, 0],
        'prediction': [1, 1, 0, 0, 1, 1, 0, 0],
        'gender': ['M', 'M', 'M', 'M', 'F', 'F', 'F', 'F']
    })
    df_fair.to_csv('test_fair.csv', index=False)
    
    res1 = runner.run('test_fair.csv', 'target', 'prediction', 'gender')
    print("Test 1 (Perfectly Fair):", res1.status)
    assert res1.status == "success"
    assert len(res1.findings) == 0, f"Expected 0 findings, got {len(res1.findings)}"
    
    # 2. Deliberately unfair synthetic data
    # Group M gets 90% positive prediction, Group F gets 20%
    # Group M: 10 people, 9 positive
    # Group F: 10 people, 2 positive
    df_unfair = pd.DataFrame({
        'target': [1]*10 + [1]*10,
        'prediction': [1]*9 + [0]*1 + [1]*2 + [0]*8,
        'gender': ['M']*10 + ['F']*10
    })
    df_unfair.to_csv('test_unfair.csv', index=False)
    
    res2 = runner.run('test_unfair.csv', 'target', 'prediction', 'gender')
    print("Test 2 (Unfair Data):", res2.status)
    assert res2.status == "success"
    assert len(res2.findings) > 0, "Expected findings due to deliberate gap"
    
    # 3. Error-path test: bad sensitive column
    res3 = runner.run('test_fair.csv', 'target', 'prediction', 'bad_column')
    print("Test 3 (Bad Column):", res3.status)
    assert res3.status == "error"
    assert "not found" in res3.summary
    
    print("All fairness tests passed!")

if __name__ == "__main__":
    run_tests()
