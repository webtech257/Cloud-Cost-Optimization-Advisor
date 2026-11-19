import boto3
import pandas as pd
from datetime import datetime
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError

def get_date_range():
    """
    Returns (start_date, end_date) in YYYY-MM-01 format required by AWS Cost Explorer.
    """
    today = datetime.today()
    
    # 12 months ago from today, starting on the 1st
    start_date = f"{today.year - 1}-{today.month:02d}-01"
    
    # 1st of next month (to capture current month-to-date spending)
    if today.month == 12:
        end_date = f"{today.year + 1}-01-01"
    else:
        end_date = f"{today.year}-{today.month + 1:02d}-01"
        
    return start_date, end_date

def generate_optimization_report(service_df: pd.DataFrame, data_dir: Path):
    """
    Generates and saves optimization_report.csv dynamically based on actual services retrieved.
    """
    if service_df.empty:
        return
        
    service_cost = service_df.groupby("Service")["Cost_USD"].sum()
    
    def get_service_meta(name: str):
        n = name.lower()
        if "ec2" in n or "compute" in n:
            return 15, "Right-size underutilized instances, apply automated stop/start scheduling, and leverage Spot instances or Savings Plans."
        elif "s3" in n or "storage" in n or "simple storage" in n:
            return 10, "Review storage classes and consider lifecycle policies (e.g., S3 Intelligent-Tiering)."
        elif "rds" in n or "database" in n or "aurora" in n:
            return 12, "Review database instance sizing, identify idle instances, and schedule non-production databases."
        elif "lambda" in n or "serverless" in n:
            return 8, "Optimize execution duration and memory allocation to minimize billed compute time."
        elif "cloudwatch" in n or "monitoring" in n:
            return 5, "Review log retention periods and delete unneeded custom metrics."
        elif "dynamodb" in n:
            return 10, "Review read/write capacity modes and switch idle tables to on-demand."
        elif "free tier" in n:
            return 0, "Account currently running within AWS Free Tier limits ($0.00 billed). Monitor usage to avoid unexpected overages."
        else:
            return 5, f"Review {name} usage and rightsizing opportunities."
            
    report = []
    for service, cost in service_cost.items():
        rate, rec = get_service_meta(service)
        savings = cost * rate / 100
        report.append({
            "Service": service,
            "Current_Cost_USD": round(cost, 2),
            "Assumed_Optimization_Percent": rate,
            "Potential_Savings_USD": round(savings, 2),
            "Illustrative_Optimized_Cost_USD": round(cost - savings, 2),
            "Recommendation": rec
        })
        
    report_df = pd.DataFrame(report)
    report_df.to_csv(data_dir / "optimization_report.csv", index=False)
    print(f"[OK] Generated optimization report for {len(report_df)} services in data/optimization_report.csv")

def fetch_real_aws_costs(include_zero_cost: bool = True):
    """
    Fetches real AWS Cost Explorer data and updates:
    - data/aws_cost_data.csv (Service-level monthly spending)
    - data/historical_cost_data.csv (Total monthly spending)
    - data/optimization_report.csv (Optimization recommendations)
    
    Returns a dict with status and summary details.
    """
    print("\nConnecting to AWS Account...")
    
    result = {
        "success": False,
        "account_id": None,
        "user_arn": None,
        "services_count": 0,
        "total_cost": 0.0,
        "message": ""
    }
    
    try:
        # 1. Validate STS Identity
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        account_id = identity.get("Account")
        user_arn = identity.get("Arn")
        result["account_id"] = account_id
        result["user_arn"] = user_arn
        print(f"Connected to AWS Account ID: {account_id} ({user_arn.split('/')[-1]})")

        # 2. Connect to Cost Explorer API (hosted in us-east-1)
        client = boto3.client("ce", region_name="us-east-1")
        
        start_date, end_date = get_date_range()
        print(f"Requesting monthly cost data from {start_date} to {end_date}...")
        
        # 3. Query Service Breakdown
        try:
            service_response = client.get_cost_and_usage(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
            )
        except ClientError as e:
            # Fall back to current month's 1st if next month's 1st is rejected as future
            if "End date" in str(e) or "ValidationException" in str(e):
                today = datetime.today()
                end_date = f"{today.year}-{today.month:02d}-01"
                service_response = client.get_cost_and_usage(
                    TimePeriod={"Start": start_date, "End": end_date},
                    Granularity="MONTHLY",
                    Metrics=["UnblendedCost"],
                    GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
                )
            else:
                raise e
        
        service_records = []
        historical_records = []
        overall_spend = 0.0
        
        for period in service_response.get("ResultsByTime", []):
            period_start = period["TimePeriod"]["Start"]
            period_total = 0.0
            
            for group in period.get("Groups", []):
                service_name = group["Keys"][0]
                cost = float(group["Metrics"]["UnblendedCost"]["Amount"])
                
                # Include service if cost > 0 or if include_zero_cost is enabled
                if cost > 0 or include_zero_cost:
                    period_total += cost
                    service_records.append({
                        "Date": period_start,
                        "Service": service_name,
                        "Usage_Type": "CloudUsage",
                        "Region": "Global/Multi-Region",
                        "Usage_Amount": 1,
                        "Cost_USD": round(cost, 2)
                    })
            
            historical_records.append({
                "Date": period_start,
                "Cost_USD": round(period_total, 2)
            })
            overall_spend += period_total
            
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        # If no groups were returned by Cost Explorer (brand new account with $0)
        if not service_records:
            today_str = datetime.today().strftime("%Y-%m-01")
            service_records.append({
                "Date": today_str,
                "Service": "AWS Free Tier / Active Account",
                "Usage_Type": "CloudUsage",
                "Region": "Global/Multi-Region",
                "Usage_Amount": 1,
                "Cost_USD": 0.0
            })
            historical_records.append({
                "Date": today_str,
                "Cost_USD": 0.0
            })
            print("\nNotice: Your AWS account currently has $0.00 spend recorded in Cost Explorer.")
            print("Recorded $0.00 Free Tier active baseline so your dashboard shows your live account.")

        # Save service breakdown CSV
        service_df = pd.DataFrame(service_records)
        service_csv_path = data_dir / "aws_cost_data.csv"
        service_df.to_csv(service_csv_path, index=False)
        print(f"[OK] Saved {len(service_df)} live AWS service records to data/{service_csv_path.name}")
        
        # Save historical totals CSV
        historical_df = pd.DataFrame(historical_records)
        hist_csv_path = data_dir / "historical_cost_data.csv"
        historical_df.to_csv(hist_csv_path, index=False)
        print(f"[OK] Saved {len(historical_df)} monthly totals to data/{hist_csv_path.name}")
        
        # Dynamically generate optimization report
        generate_optimization_report(service_df, data_dir)
        
        # Automatically update forecast data and model for live account
        try:
            monthly_data = (
                service_df.groupby(pd.to_datetime(service_df["Date"]).dt.to_period("M"))["Cost_USD"]
                .sum()
                .reset_index()
            )
            monthly_data["Date"] = monthly_data["Date"].dt.to_timestamp()
            forecast_data = monthly_data.rename(columns={"Date": "ds", "Cost_USD": "y"})
            forecast_data.to_csv(data_dir / "forecast_data.csv", index=False)
            
            from prophet import Prophet
            m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
            m.fit(forecast_data)
            future = m.make_future_dataframe(periods=3, freq="MS")
            forecast = m.predict(future)
            forecast.to_csv(data_dir / "forecast_results.csv", index=False)
            print("[OK] Retrained Prophet forecast model on live AWS billing data.")
        except Exception as fe:
            print(f"[NOTE] Forecast model retrain note: {fe}")
        
        result["success"] = True
        result["services_count"] = len(service_df["Service"].unique())
        result["total_cost"] = round(overall_spend, 2)
        result["message"] = f"Successfully synced live billing from AWS Account {account_id}! Total Spend: ${overall_spend:.2f}"
        print(f"\nSUCCESS! {result['message']}")
        return result
        
    except NoCredentialsError:
        msg = "AWS credentials not found. Please run 'aws configure' in terminal."
        print(f"\n[ERROR] {msg}")
        result["message"] = msg
        return result
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_msg = e.response.get("Error", {}).get("Message", str(e))
        msg = f"AWS {error_code}: {error_msg}"
        print(f"\n[AWS ERROR] {msg}")
        result["message"] = msg
        return result
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        print(f"\n[ERROR] {msg}")
        result["message"] = msg
        return result

if __name__ == "__main__":
    fetch_real_aws_costs(include_zero_cost=True)
    fetch_real_aws_costs(include_zero_cost=True)
