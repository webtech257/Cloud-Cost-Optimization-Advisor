
import pandas as pd
from prophet import Prophet
from pathlib import Path

# Load prepared forecasting data
file_path = Path(__file__).parent / "data" / "forecast_data.csv"
df = pd.read_csv(file_path)

# Create Prophet model
model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=False,
    daily_seasonality=False
)

# Train the model
model.fit(df)

print("\nProphet model trained successfully!")

# Generate future dates
future = model.make_future_dataframe(
    periods=3,
    freq="MS"
)

# Predict future AWS spending
forecast = model.predict(future)

# Display predictions
print("\n====== AWS COST FORECAST ======")

print(
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    .tail(3)
)

# Save forecast results
output_path = Path(__file__).parent / "data" / "forecast_results.csv"
forecast.to_csv(output_path, index=False)

print("\nForecast results saved successfully!")
