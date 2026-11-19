
import pandas as pd
from pathlib import Path

# Load AWS cost dataset
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

# Calculate total cost by service
service_cost = df.groupby("Service")["Cost_USD"].sum()

# Assumed optimization percentages for demonstration
optimization_rates = {
    "Amazon EC2": 15,
    "Amazon S3": 10,
    "Amazon RDS": 12,
    "AWS Lambda": 8,
    "Amazon CloudWatch": 5
}

total_savings = 0

print("\n====== ESTIMATED CLOUD COST SAVINGS ======")

for service, cost in service_cost.items():

    rate = optimization_rates.get(service, 0)

    # Calculate potential savings
    savings = cost * rate / 100

    optimized_cost = cost - savings

    total_savings += savings

    print("\nService:", service)
    print("Current Cost:", f"${cost:.2f}")
    print("Assumed Optimization:", f"{rate}%")
    print("Potential Savings:", f"${savings:.2f}")
    print("Illustrative Optimized Cost:", f"${optimized_cost:.2f}")

# Calculate total savings
total_cost = service_cost.sum()

print("\n====== OVERALL SAVINGS SUMMARY ======")
print("Current Total Cost:", f"${total_cost:.2f}")
print("Potential Total Savings:", f"${total_savings:.2f}")
print("Illustrative Optimized Cost:", f"${total_cost - total_savings:.2f}")

print("\nSavings analysis completed!")
