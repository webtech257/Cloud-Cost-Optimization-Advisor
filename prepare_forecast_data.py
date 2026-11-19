
import pandas as pd
from pathlib import Path

# Load AWS cost dataset
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Group spending by month
monthly_data = (
    df.groupby(df["Date"].dt.to_period("M"))["Cost_USD"]
    .sum()
    .reset_index()
)

# Prepare Prophet format
monthly_data["Date"] = monthly_data["Date"].dt.to_timestamp()

forecast_data = monthly_data.rename(
    columns={
        "Date": "ds",
        "Cost_USD": "y"
    }
)

# Display prepared data
print("\n====== DATA PREPARED FOR PROPHET ======")
print(forecast_data)

# Save prepared dataset
output_path = Path(__file__).parent / "data" / "forecast_data.csv"
forecast_data.to_csv(output_path, index=False)

print("\nForecast dataset saved successfully!")
