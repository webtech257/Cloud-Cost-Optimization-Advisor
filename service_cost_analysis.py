
import pandas as pd
from pathlib import Path

# Load AWS cost dataset
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

# Calculate total cost for each AWS service
service_cost = df.groupby("Service")["Cost_USD"].sum()

# Sort services from highest cost to lowest cost
service_cost = service_cost.sort_values(ascending=False)

# Display results
print("\n====== AWS SERVICE-WISE COST ANALYSIS ======")
print(service_cost)

# Identify the most expensive service
highest_service = service_cost.idxmax()
highest_cost = service_cost.max()

print("\n====== COST INSIGHT ======")
print("Most expensive service:", highest_service)
print("Total cost:", f"${highest_cost:.2f}")

# Calculate overall spending
total_cost = df["Cost_USD"].sum()

print("\nTotal AWS spending:", f"${total_cost:.2f}")

import matplotlib.pyplot as plt

# Create a bar chart
plt.figure(figsize=(10, 5))

service_cost.plot(kind="bar")

plt.title("AWS Service-wise Cost Analysis")
plt.xlabel("AWS Services")
plt.ylabel("Total Cost (USD)")

plt.xticks(rotation=30)
plt.tight_layout()

# Display the graph
plt.show()

