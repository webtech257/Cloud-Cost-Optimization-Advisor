# Cloud Cost Optimization Advisor ☁️

An intelligent, machine-learning-powered FinOps dashboard and analytics platform for monitoring AWS cloud spending, forecasting future expenditures with Facebook Prophet, identifying statistical anomalies using Isolation Forest, and providing automated rightsizing recommendations.

---

## 📁 Project Directory Organization

```text
Cloud-Cost-Optimization-Advisor/
│
├── .streamlit/
│   └── config.toml                  # Streamlit dark SaaS theme configuration
│
├── data/                            # Datasets and model outputs
│   ├── aws_cost_data.csv            # Service-wise monthly billing records
│   ├── historical_cost_data.csv     # Historical spending progression
│   ├── forecast_data.csv            # Cleaned data prepared for Prophet
│   ├── forecast_results.csv         # Prophet predictions with confidence intervals
│   ├── optimization_report.csv      # FinOps rightsizing report and savings breakdown
│   ├── cost_anomaly_results.csv     # Detected cost outliers and labels
│   └── anomaly_evaluation_results.csv # Ground truth vs. predicted evaluation data
│
├── ui/                              # Modular UI & Design System
│   ├── __init__.py                  # UI package marker
│   ├── styles.py                    # Consolidated dark glassmorphic CSS styling
│   ├── charts.py                    # Plotly chart builders (bar, donut, area, scatter)
│   ├── components.py                # Reusable UI components (hero, sidebar, headers, footer)
│   └── icons.py                     # Inline SVG feather/lucide icons
│
├── app.py                           # Main Streamlit web application
├── fetch_aws_cost_data.py           # Live AWS Cost Explorer data extractor
├── test_aws_connection.py           # AWS STS connection validator
├── requirements.txt                 # Project dependencies
└── .gitignore                       # Git ignore rules for venv, pycache, and secrets
│
├── 📊 Cost Analysis & Visualization
│   ├── load_cost_data.py            # Loads and validates AWS cost datasets
│   ├── service_cost_analysis.py     # Aggregates spending by AWS service
│   ├── monthly_cost_analysis.py     # Computes monthly billing trends
│   └── cost_visualization.py        # Matplotlib baseline charts
│
├── 💡 Optimization & Recommendations
│   ├── recommendation_engine.py     # Rule-based rightsizing suggestions
│   ├── cost_savings.py              # Potential savings calculations
│   └── optimization_report.py       # Generates data/optimization_report.csv
│
├── 📈 Machine Learning Forecasting (Prophet)
│   ├── prepare_forecast_data.py     # Transforms monthly costs for Prophet (ds, y)
│   ├── train_forecast_model.py      # Trains Prophet and generates 3-month forecast
│   ├── evaluate_forecast.py         # Evaluates model performance (MAE, RMSE)
│   └── visualize_forecast.py        # Plots forecast curves with uncertainty bands
│
├── 🚨 Anomaly Detection (Isolation Forest)
│   ├── cost_anomaly_detection.py    # Trains Isolation Forest to detect spending spikes
│   └── evaluate_anomaly_model.py    # Generates Confusion Matrix, Precision, Recall, F1
│
└── 🧪 Automated Test Suites
    ├── test_cost_analysis.py        # Validates data integrity & totals
    ├── test_optimization.py         # Validates savings and rightsizing calculations
    ├── test_anomaly_detection.py    # Validates anomaly flags and status labels
    └── test_phase9.py               # Comprehensive Phase 9 end-to-end test suite
```

---

## 🚀 Getting Started

### 1. Prerequisites & Virtual Environment
Ensure you have Python 3.10+ installed. Activate your virtual environment:

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:
```powershell
pip install -r requirements.txt
```

### 2. Running the Dashboard
Launch the Streamlit dashboard in your browser:
```powershell
streamlit run app.py
```

### 3. Running Test Suites
Verify all calculations and pipeline phases:
```powershell
python test_cost_analysis.py
python test_optimization.py
python test_anomaly_detection.py
python test_phase9.py
```

### 4. Optional: Connecting to Live AWS Account
To pull live data from your own AWS account:
1. Configure credentials: `aws configure` (Region: `us-east-1` or your default region).
2. Validate connection: `python test_aws_connection.py`
3. Fetch live records: `python fetch_aws_cost_data.py`
4. Re-launch `streamlit run app.py`
