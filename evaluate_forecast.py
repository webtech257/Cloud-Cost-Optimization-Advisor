import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path
import numpy as np

# Load historical data
file_path = Path(__file__).parent / "data" / "historical_cost_data.csv"
df = pd.read_csv(file_path)

# Prepare Prophet format
df["Date"] = pd.to_datetime(df["Date"])
df = df.rename(columns={
    "Date": "ds",
    "Cost_USD": "y"
})

# Split into training and testing data
train = df.iloc[:-6]
test = df.iloc[-6:]

# Train model using first 18 months
model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=False,
    daily_seasonality=False
)

model.fit(train)

# Predict the next 6 months
future = model.make_future_dataframe(
    periods=6,
    freq="MS"
)

forecast = model.predict(future)

# Select predictions for test period
predictions = forecast.tail(6)["yhat"].values
actual = test["y"].values

# Calculate evaluation metrics
mae = mean_absolute_error(actual, predictions)
rmse = np.sqrt(mean_squared_error(actual, predictions))

print("\n====== MODEL EVALUATION ======")
print("Actual values:", actual)
print("Predicted values:", predictions.round(2))

print("\nMean Absolute Error (MAE):", round(mae, 2))
print("Root Mean Squared Error (RMSE):", round(rmse, 2))
