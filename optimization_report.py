
import pandas as pd
from pathlib import Path

# Load AWS cost dataset
base_path = Path(__file__).parent
file_path = base_path / "data" / "aws_cost_data.csv"

df = pd.read_csv(file_path)

# Calculate service-wise cost
service_cost = df.groupby("Service")["Cost_USD"].sum()

# Optimization percentages (illustrative assumptions)
optimization_rates = {
    "Amazon EC2": 15,
    "Amazon S3": 10,
    "Amazon RDS": 12,
    "AWS Lambda": 8,
    "Amazon CloudWatch": 5
}

# Recommendations
recommendations = {
    "Amazon EC2": "Right-size underutilized instances, apply automated stop/start scheduling, and leverage Spot instances or Savings Plans.",
    "Amazon S3": "Review storage classes and configure lifecycle policies (e.g., S3 Intelligent-Tiering).",
    "Amazon RDS": "Review database instance sizing and apply automated scheduling for non-production environments.",
    "AWS Lambda": "Optimize execution duration and memory allocation to reduce billed execution time.",
    "Amazon CloudWatch": "Review log retention periods and eliminate unneeded custom metrics."
}

report = []

total_cost = 0
total_savings = 0

# Generate report records
for service, cost in service_cost.items():

    rate = optimization_rates.get(service, 0)
    savings = cost * rate / 100
    optimized_cost = cost - savings

    total_cost += cost
    total_savings += savings

    report.append({
        "Service": service,
        "Current_Cost_USD": round(cost, 2),
        "Assumed_Optimization_Percent": rate,
        "Potential_Savings_USD": round(savings, 2),
        "Illustrative_Optimized_Cost_USD": round(optimized_cost, 2),
        "Recommendation": recommendations.get(service, "Review service usage.")
    })

# Convert to DataFrame
report_df = pd.DataFrame(report)

# Display report
print("\n====== CLOUD COST OPTIMIZATION REPORT ======")
print(report_df.to_string(index=False))

print("\n====== OVERALL SUMMARY ======")
print("Total Current Cost:", f"${total_cost:.2f}")
print("Potential Savings:", f"${total_savings:.2f}")
print("Illustrative Optimized Cost:", f"${total_cost - total_savings:.2f}")

# Save report
output_path = base_path / "data" / "optimization_report.csv"
report_df.to_csv(output_path, index=False)

print("\nOptimization report saved successfully!")
