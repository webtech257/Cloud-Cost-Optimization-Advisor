
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest

# Load historical AWS cost data
base_path = Path(__file__).parent
file_path = base_path / "data" / "historical_cost_data.csv"

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

# Real AWS historical dataset
test_df = df.copy()

# Create month number as a feature
test_df["Month_Number"] = range(1, len(test_df) + 1)

# Select machine learning features
X = test_df[["Month_Number", "Cost_USD"]]

# Create Isolation Forest model
model = IsolationForest(
    contamination=0.10,
    random_state=42
)

# Detect anomalies on real AWS data
test_df["Anomaly"] = model.fit_predict(X)

# Convert model results into readable labels
test_df["Status"] = test_df["Anomaly"].map({
    1: "Normal",
    -1: "Anomaly Detected"
})

# Display results
print("\n====== AWS COST ANOMALY DETECTION ======")

print(
    test_df[["Date", "Cost_USD", "Status"]].to_string(index=False)
)

# Display detected anomalies
anomalies = test_df[test_df["Anomaly"] == -1]

print("\n====== DETECTED ANOMALIES ======")

if not anomalies.empty:
    print(anomalies[["Date", "Cost_USD", "Status"]].to_string(index=False))
else:
    print("No anomalies detected.")

# Save results
output_path = base_path / "data" / "cost_anomaly_results.csv"

test_df.to_csv(output_path, index=False)

print("\nAnomaly detection results saved successfully!")
