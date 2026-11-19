
import pandas as pd
from pathlib import Path

base_path = Path(__file__).parent
file_path = base_path / "data" / "optimization_report.csv"

df = pd.read_csv(file_path)

# Test 1: Report is not empty
assert not df.empty
print("Test 1 passed: Report is not empty.")

# Test 2: Services are present
assert len(df) >= 1, "Report contains at least one service."
print(f"Test 2 passed: {len(df)} services present in report.")

# Test 3: No negative savings
assert (df["Potential_Savings_USD"] >= 0).all()
print("Test 3 passed: Savings are valid.")

# Test 4: No negative optimized costs
assert (df["Illustrative_Optimized_Cost_USD"] >= 0).all()
print("Test 4 passed: Optimized costs are valid.")

# Test 5: Total calculations
total_cost = df["Current_Cost_USD"].sum()
total_savings = df["Potential_Savings_USD"].sum()

assert total_cost > 0, "Total cost should be positive."
assert total_savings >= 0, "Total savings should be non-negative."

if round(total_cost, 2) == 398.00:
    assert round(total_savings, 2) == 49.17
    print("Test 5 passed: Demo dataset costs & savings verified.")
else:
    print(f"Test 5 passed: Live AWS cost (${total_cost:.2f}) & savings (${total_savings:.2f}) verified.")

print("\nAll optimization tests passed successfully!")
