
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

# Calculate service-wise spending
service_cost = df.groupby("Service")["Cost_USD"].sum()
service_cost = service_cost.sort_values(ascending=False)

# Calculate monthly spending
monthly_cost = df.groupby("Month")["Cost_USD"].sum()

# Overall spending
total_cost = df["Cost_USD"].sum()

# Create two graphs
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Graph 1: Service-wise cost
service_cost.plot(
    kind="bar",
    ax=axes[0],
    title="AWS Service-wise Spending"
)

axes[0].set_xlabel("AWS Services")
axes[0].set_ylabel("Cost (USD)")
axes[0].tick_params(axis="x", rotation=30)

# Graph 2: Monthly cost
monthly_cost.plot(
    kind="line",
    marker="o",
    ax=axes[1],
    title="Monthly AWS Spending Trend"
)

axes[1].set_xlabel("Month")
axes[1].set_ylabel("Cost (USD)")
axes[1].grid(True)

# Overall title
fig.suptitle(
    f"AWS Cost Analysis Dashboard | Total: ${total_cost:.2f}"
)

plt.tight_layout()
plt.show()

print("\nTotal AWS Spending:", f"${total_cost:.2f}")
print("Visualization completed successfully!")
