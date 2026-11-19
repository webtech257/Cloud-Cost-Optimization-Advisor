
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load AWS cost data
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

# Convert Date into datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Group costs by month
df["Month"] = df["Date"].dt.to_period("M")

monthly_cost = df.groupby("Month")["Cost_USD"].sum()

print("\n====== MONTHLY AWS SPENDING ======")
print(monthly_cost)

# Calculate spending increase
if len(monthly_cost) >= 2:
    first_month = monthly_cost.iloc[0]
    last_month = monthly_cost.iloc[-1]

    increase = last_month - first_month
    percentage = (increase / first_month) * 100

    print("\n====== SPENDING INSIGHT ======")
    print(f"Spending increase: ${increase:.2f}")
    print(f"Percentage change: {percentage:.2f}%")

# Create monthly spending graph
plt.figure(figsize=(9, 5))

monthly_cost.plot(kind="line", marker="o")

plt.title("Monthly AWS Spending Trend")
plt.xlabel("Month")
plt.ylabel("Total Cost (USD)")
plt.grid(True)
plt.tight_layout()

plt.show()
