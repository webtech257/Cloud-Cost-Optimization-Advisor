
import pandas as pd
from pathlib import Path

# Load AWS cost data
file_path = Path(__file__).parent / "data" / "aws_cost_data.csv"
df = pd.read_csv(file_path)

# Calculate total spending by service
service_cost = df.groupby("Service")["Cost_USD"].sum()

# Define optimization recommendations
recommendations = {
    "Amazon EC2":
        "Right-size underutilized instances, implement automated off-hours scheduling for dev/test environments, and leverage EC2 Spot instances or Savings Plans.",

    "Amazon S3":
        "Review storage classes and configure S3 Intelligent-Tiering and lifecycle policies for infrequently accessed objects.",

    "Amazon RDS":
        "Review database instance sizing, identify idle or over-provisioned clusters, and schedule non-production databases.",

    "AWS Lambda":
        "Optimize execution memory allocation and function duration to minimize billed duration GB-seconds.",

    "Amazon CloudWatch":
        "Review log retention periods and eliminate unneeded custom metrics and frequent alarm polling."
}

print("\n====== CLOUD COST OPTIMIZATION RECOMMENDATIONS ======")

# Generate recommendations
for service, cost in service_cost.items():

    recommendation = recommendations.get(
        service,
        "Review this service's usage and pricing."
    )

    print("\nService:", service)
    print("Total Cost:", f"${cost:.2f}")
    print("Recommendation:", recommendation)

print("\nRecommendation engine executed successfully!")

