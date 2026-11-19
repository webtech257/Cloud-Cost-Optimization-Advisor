
import pandas as pd
from pathlib import Path

base_path = Path(__file__).parent

file_path = base_path / "data" / "cost_anomaly_results.csv"

df = pd.read_csv(file_path)

# Test 1: Dataset is not empty
assert not df.empty
print("Test 1 passed: Dataset is not empty.")

# Test 2: Required columns exist
required_columns = [
    "Date",
    "Cost_USD",
    "Anomaly",
    "Status"
]

for column in required_columns:
    assert column in df.columns

print("Test 2 passed: Required columns exist.")

# Test 3: No negative costs
assert (df["Cost_USD"] >= 0).all()
print("Test 3 passed: No negative costs.")

# Test 4: Status labels are valid
valid_statuses = ["Normal", "Anomaly Detected"]

assert df["Status"].isin(valid_statuses).all()
print("Test 4 passed: Status labels are valid.")

# Test 5: At least one anomaly detected
anomalies = df[df["Status"] == "Anomaly Detected"]

assert not anomalies.empty

print("Test 5 passed: Anomalies detected.")

# Display detected records
print("\nDetected anomalies:")
print(anomalies[["Date", "Cost_USD", "Status"]])

print("\nAll anomaly detection tests passed!")
