
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
        "Review EC2 instance utilization and consider right-sizing oversized instances.",

    "Amazon S3":
        "Review storage classes and consider lifecycle policies for infrequently accessed data.",

    "Amazon RDS":
        "Review database instance sizing and identify opportunities for optimization.",

    "AWS Lambda":
        "Review execution duration and memory allocation to optimize Lambda costs.",

    "Amazon CloudWatch":
        "Review log retention periods and unnecessary monitoring metrics."
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

