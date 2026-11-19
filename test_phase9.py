
import pandas as pd
from pathlib import Path

base_path = Path(__file__).parent
data_path = base_path / "data"

# Test 1: Anomaly detection results
anomaly_file = data_path / "cost_anomaly_results.csv"
assert anomaly_file.exists()

anomaly_df = pd.read_csv(anomaly_file)
assert not anomaly_df.empty

print("Test 1 passed: Anomaly results generated.")

# Test 2: Anomaly status validation
assert "Status" in anomaly_df.columns
assert anomaly_df["Status"].isin(
    ["Normal", "Anomaly Detected"]
).all()

print("Test 2 passed: Anomaly status is valid.")

# Test 3: At least one anomaly
assert (anomaly_df["Status"] == "Anomaly Detected").any()

print("Test 3 passed: Anomaly detected.")

# Test 4: Evaluation results
evaluation_file = data_path / "anomaly_evaluation_results.csv"
assert evaluation_file.exists()

evaluation_df = pd.read_csv(evaluation_file)

assert {"Actual", "Predicted"}.issubset(
    evaluation_df.columns
)

print("Test 4 passed: Evaluation results generated.")

# Test 5: Prediction values
assert evaluation_df["Predicted"].isin([0, 1]).all()

print("Test 5 passed: Predictions are valid.")

# Test 6: Evaluation data is complete
assert len(evaluation_df) == len(anomaly_df) and len(evaluation_df) > 0
assert evaluation_df["Actual"].isin([0, 1]).all()

print("Test 6 passed: Evaluation dataset is valid.")

print("\nAll 6 Phase 9 tests passed successfully!")
