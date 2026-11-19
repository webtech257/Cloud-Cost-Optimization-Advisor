
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load actual historical data
base_path = Path(__file__).parent

actual = pd.read_csv(base_path / "data" / "forecast_data.csv")
forecast = pd.read_csv(base_path / "data" / "forecast_results.csv")

# Convert dates
actual["ds"] = pd.to_datetime(actual["ds"])
forecast["ds"] = pd.to_datetime(forecast["ds"])

# Create graph
plt.figure(figsize=(11, 6))

# Historical spending
plt.plot(
    actual["ds"],
    actual["y"],
    marker="o",
    label="Actual AWS Cost"
)

# Predicted spending
plt.plot(
    forecast["ds"],
    forecast["yhat"],
    linestyle="--",
    marker="o",
    label="Predicted AWS Cost"
)

# Forecast uncertainty range
plt.fill_between(
    forecast["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.2,
    label="Uncertainty Range"
)

# Graph formatting
plt.title("AWS Cost Forecast using Prophet")
plt.xlabel("Date")
plt.ylabel("Cost (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()

print("Forecast visualization completed!")
