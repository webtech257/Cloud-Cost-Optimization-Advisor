
import pandas as pd
from pathlib import Path

# Find the CSV file
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"

# Load CSV data
df = pd.read_csv(file_path)

# Convert Date column into date format
df["Date"] = pd.to_datetime(df["Date"])

# Display the dataset
print("\n========== AWS COST DATA ==========")
print(df)

# Display basic information
print("\n========== DATA INFORMATION ==========")
print(df.info())

# Display statistical summary
print("\n========== COST SUMMARY ==========")
print(df["Cost_USD"].describe())

print("\nDataset loaded successfully!")
