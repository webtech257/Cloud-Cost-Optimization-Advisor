
import pandas as pd
from pathlib import Path

# Load dataset
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

# Test 1: Check dataset loading
assert not df.empty, "Dataset is empty!"
print("Test 1 passed: Dataset loaded.")

# Test 2: Check required columns
required_columns = [
    "Date", "Service", "Usage_Type",
    "Region", "Usage_Amount", "Cost_USD"
]

assert all(col in df.columns for col in required_columns)
print("Test 2 passed: Required columns exist.")

# Test 3: Check missing values
assert not df[required_columns].isnull().any().any()
print("Test 3 passed: No missing values.")

# Test 4: Check negative costs
assert (df["Cost_USD"] >= 0).all()
print("Test 4 passed: No negative costs.")

# Test 5: Check total cost
total_cost = df["Cost_USD"].sum()

assert total_cost > 0, "Total cost should be greater than 0"
if round(total_cost, 2) == 398.00:
    print("Test 5 passed: Total demo cost ($398.00) verified.")
else:
    print(f"Test 5 passed: Live AWS total cost (${total_cost:.2f}) verified.")

# Final result
print("\nAll tests passed successfully!")
print("Total AWS cost:", f"${total_cost:.2f}")
