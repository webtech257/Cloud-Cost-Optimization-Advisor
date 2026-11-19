
import pandas as pd
from pathlib import Path

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

base_path = Path(__file__).parent

file_path = base_path / "data" / "historical_cost_data.csv"

df = pd.read_csv(file_path)

# Prepare test data
df["Date"] = pd.to_datetime(df["Date"])
df["Month_Number"] = range(1, len(df) + 1)

# Statistical ground-truth baseline on real AWS data:
# Flag statistical outliers exceeding 1.5 standard deviations from the mean
mean_cost = df["Cost_USD"].mean()
std_cost = df["Cost_USD"].std()
df["Actual"] = ((df["Cost_USD"] - mean_cost).abs() > 1.5 * std_cost).astype(int)

# Machine learning features
X = df[["Month_Number", "Cost_USD"]]

# Train Isolation Forest
model = IsolationForest(
    contamination=0.10,
    random_state=42
)

predictions = model.fit_predict(X)

# Convert predictions: -1 -> Anomaly (1), 1 -> Normal (0)
df["Predicted"] = (predictions == -1).astype(int)

# Evaluation
print("\n====== ANOMALY MODEL EVALUATION ======")

print("\nConfusion Matrix:")
print(confusion_matrix(df["Actual"], df["Predicted"]))

print("\nClassification Report:")
print(
    classification_report(
        df["Actual"],
        df["Predicted"],
        target_names=["Normal", "Anomaly"],
        zero_division=0
    )
)

# Save evaluation results
output_path = base_path / "data" / "anomaly_evaluation_results.csv"

df.to_csv(output_path, index=False)

print("\nAnomaly evaluation results saved successfully!")
