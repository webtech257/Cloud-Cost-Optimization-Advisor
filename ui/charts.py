"""
Plotly Chart Builders for Cloud Cost Optimization Advisor.
Custom dark SaaS theme, transparent backgrounds, glowing highlights, and rich hover tooltips.
Supports dynamic currency formatting and conversion (USD $, INR ₹, etc.).
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#a5a8c8", size=12),
    margin=dict(l=20, r=20, t=25, b=25),
    hoverlabel=dict(
        bgcolor="#11122b",
        bordercolor="#8b5cf6",
        font=dict(family="Inter, sans-serif", color="#f1f2ff", size=12)
    )
)

def create_service_cost_chart(service_cost: pd.Series, symbol: str = "$", rate: float = 1.0) -> go.Figure:
    """
    Builds a premium horizontal bar chart of AWS Service costs.
    Filters out zero-cost items so active spending services are clearly legible.
    The highest-cost service is highlighted with a vivid magenta/violet glow and badge annotation.
    Supports currency scaling and custom currency symbol.
    """
    # Filter to active spending services (> $0.00) if any exist
    active_cost = service_cost[service_cost > 0]
    target_series = active_cost if not active_cost.empty else service_cost

    # Sort ascending so highest appears at the top of horizontal bar chart
    sorted_series = target_series.sort_values(ascending=True)
    services = sorted_series.index.tolist()
    costs = (sorted_series * rate).values.tolist()
    total = sum(costs) if sum(costs) > 0 else 1.0
    percentages = [(c / total) * 100 for c in costs]
    
    max_cost = max(costs) if costs else 0
    
    # Custom color palette: highlight max
    colors = []
    line_colors = []
    line_widths = []
    for c in costs:
        if c == max_cost and c > 0:
            colors.append("rgba(168, 85, 247, 0.95)")  # Vivid violet/purple
            line_colors.append("#f1f2ff")
            line_widths.append(1.5)
        else:
            colors.append("rgba(99, 102, 241, 0.65)")   # Electric indigo
            line_colors.append("rgba(167, 139, 250, 0.3)")
            line_widths.append(1)
            
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=services,
        x=costs,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color=line_colors, width=line_widths),
            cornerradius=6
        ),
        customdata=percentages,
        hovertemplate=f"<b>%{{y}}</b><br>Cost: {symbol}%{{x:,.2f}}<br>Share: %{{customdata:.1f}}%<extra></extra>",
        showlegend=False
    ))
    
    # Annotate highest cost
    if max_cost > 0:
        max_idx = costs.index(max_cost)
        max_service = services[max_idx]
        fig.add_annotation(
            x=max_cost,
            y=max_service,
            text=f"Highest: {symbol}{max_cost:,.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor="#c084fc",
            ax=50,
            ay=0,
            font=dict(color="#f1f2ff", size=10, family="Inter, sans-serif"),
            bgcolor="rgba(139, 92, 246, 0.4)",
            bordercolor="rgba(167, 139, 250, 0.6)",
            borderwidth=1,
            borderpad=4
        )
        
    layout_kwargs = dict(CHART_LAYOUT)
    layout_kwargs.update(
        height=360,
        margin=dict(l=20, r=25, t=25, b=25),
        xaxis=dict(
            tickprefix=symbol,
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#a5a8c8", size=11)
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="#f1f2ff", size=11, family="Inter, sans-serif")
        )
    )
    fig.update_layout(**layout_kwargs)
    return fig

def create_service_donut_chart(service_cost: pd.Series, symbol: str = "$", rate: float = 1.0) -> go.Figure:
    """
    Builds a modern donut chart showing percentage distribution of cloud services.
    Filters out $0 services and bundles minor services to ensure the legend never overlaps.
    Supports currency scaling and custom currency symbol.
    """
    # 1. Filter to active spending services (> $0.00)
    active_cost = service_cost[service_cost > 0].sort_values(ascending=False)
    
    # Handle zero-cost edge case (e.g. Free Tier)
    if active_cost.empty:
        chart_series = pd.Series({"AWS Free Tier": 1.0})
        total = 0.0
    elif len(active_cost) > 5:
        # Bundle beyond top 5 into 'Other Services' to prevent legend collision
        top5 = active_cost.head(5)
        others_val = active_cost.iloc[5:].sum()
        if others_val > 0:
            others = pd.Series({"Other Services": others_val})
            chart_series = pd.concat([top5, others])
        else:
            chart_series = top5
        total = active_cost.sum()
    else:
        chart_series = active_cost
        total = active_cost.sum()
        
    labels = chart_series.index.tolist()
    values = (chart_series * rate).values.tolist()
    scaled_total = total * rate
    
    palette = [
        "#8b5cf6",  # Vivid Violet
        "#3b82f6",  # Electric Blue
        "#22d3ee",  # Cyan Accent
        "#a855f7",  # Purple
        "#34d399",  # Emerald Green
        "#f59e0b",  # Amber
        "#ec4899"   # Pink
    ]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        domain=dict(x=[0, 1], y=[0.24, 1.0]),  # Confine donut to upper 76% of canvas
        marker=dict(
            colors=palette[:len(labels)],
            line=dict(color="#0a0b1e", width=2)
        ),
        textinfo="percent",
        textposition="inside",
        insidetextorientation="horizontal",
        textfont=dict(color="#ffffff", size=11, family="Inter, sans-serif"),
        hovertemplate=f"<b>%{{label}}</b><br>Cost: {symbol}%{{value:,.2f}}<br>Share: %{{percent}}<extra></extra>"
    )])
    
    layout_kwargs = dict(CHART_LAYOUT)
    layout_kwargs.update(
        height=360,
        margin=dict(l=15, r=15, t=15, b=20),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.18,              # Position cleanly below the donut (which ends at y=0.24)
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#a5a8c8", family="Inter, sans-serif")
        ),
        annotations=[dict(
            text=f"Total<br><b>{symbol}{scaled_total:,.2f}</b>",
            x=0.5,
            y=0.62,              # Center of donut: (0.24 + 1.0) / 2 = 0.62
            font=dict(size=13, color="#f1f2ff", family="Space Grotesk, sans-serif"),
            showarrow=False
        )]
    )
    fig.update_layout(**layout_kwargs)
    return fig

def create_monthly_trend_chart(monthly_cost: pd.Series, symbol: str = "$", rate: float = 1.0) -> go.Figure:
    """
    Builds a spline area-line chart for monthly AWS spending trends.
    Supports currency scaling and custom currency symbol.
    """
    dates = [str(d) for d in monthly_cost.index]
    costs = (monthly_cost * rate).values.tolist()
    
    fig = go.Figure()
    
    # Area fill under line
    fig.add_trace(go.Scatter(
        x=dates,
        y=costs,
        mode="lines+markers",
        name="Monthly Cost",
        line=dict(shape="spline", color="#8b5cf6", width=3),
        fill="tozeroy",
        fillcolor="rgba(139, 92, 246, 0.15)",
        marker=dict(size=8, color="#c084fc", line=dict(color="#ffffff", width=1.5)),
        hovertemplate=f"<b>%{{x}}</b><br>Spend: {symbol}%{{y:,.2f}}<extra></extra>"
    ))
    
    # Annotate peak month
    if costs:
        peak_idx = int(np.argmax(costs))
        peak_val = costs[peak_idx]
        peak_date = dates[peak_idx]
        fig.add_annotation(
            x=peak_date,
            y=peak_val,
            text=f"Peak: {symbol}{peak_val:,.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor="#34d399",
            ax=0,
            ay=-35,
            font=dict(color="#f1f2ff", size=11, family="Inter, sans-serif"),
            bgcolor="rgba(16, 185, 129, 0.35)",
            bordercolor="rgba(52, 211, 153, 0.6)",
            borderwidth=1,
            borderpad=4
        )
        
    fig.update_layout(
        **CHART_LAYOUT,
        height=320,
        hovermode="x unified",
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            tickfont=dict(color="#a5a8c8", size=11),
            tickangle=-20
        ),
        yaxis=dict(
            tickprefix=symbol,
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#a5a8c8", size=11)
        )
    )
    return fig

def create_forecast_chart(forecast_df: pd.DataFrame, historical_df: pd.DataFrame = None, symbol: str = "$", rate: float = 1.0) -> go.Figure:
    """
    Builds an interactive forecast chart showing predicted yhat with translucent confidence band.
    Supports currency scaling and custom currency symbol.
    """
    fig = go.Figure()
    
    # Check if forecast_df has ds column or index
    if "ds" in forecast_df.columns:
        dates = pd.to_datetime(forecast_df["ds"])
    else:
        dates = pd.to_datetime(forecast_df.index)
        
    yhat = forecast_df["yhat"].values * rate
    yhat_lower = (forecast_df["yhat_lower"].values if "yhat_lower" in forecast_df.columns else forecast_df["yhat"].values) * rate
    yhat_upper = (forecast_df["yhat_upper"].values if "yhat_upper" in forecast_df.columns else forecast_df["yhat"].values) * rate
    
    # Shaded confidence band (yhat_lower to yhat_upper)
    fig.add_trace(go.Scatter(
        x=dates,
        y=yhat_lower,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=yhat_upper,
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(139, 92, 246, 0.16)",
        name="Confidence Interval",
        hovertemplate=f"Upper Bound: {symbol}%{{y:,.2f}}<extra></extra>"
    ))
    
    # Predicted curve (dashed electric blue)
    fig.add_trace(go.Scatter(
        x=dates,
        y=yhat,
        mode="lines+markers",
        name="Predicted Spend (yhat)",
        line=dict(color="#22d3ee", width=3, dash="dash"),
        marker=dict(size=6, color="#22d3ee", line=dict(color="#ffffff", width=1)),
        hovertemplate=f"<b>Predicted</b><br>Date: %{{x|%b %Y}}<br>Spend: {symbol}%{{y:,.2f}}<extra></extra>"
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        height=360,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#f1f2ff", size=11)
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            tickformat="%b %Y",
            tickfont=dict(color="#a5a8c8", size=11)
        ),
        yaxis=dict(
            tickprefix=symbol,
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#a5a8c8", size=11)
        )
    )
    return fig

def create_anomaly_scatter_chart(anomaly_df: pd.DataFrame, symbol: str = "$", rate: float = 1.0) -> go.Figure:
    """
    Builds a robust anomaly detection scatter/line chart.
    Correctly scales the Y-axis and highlights anomalies with glowing red badges.
    Supports currency scaling and custom currency symbol.
    """
    df = anomaly_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["Cost_Display"] = df["Cost_USD"] * rate
    
    normal_points = df[df["Status"] == "Normal"]
    anomaly_points = df[df["Status"] == "Anomaly Detected"]
    
    fig = go.Figure()
    
    # Baseline line across all dates
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Cost_Display"],
        mode="lines",
        line=dict(color="rgba(139, 92, 246, 0.35)", width=2, dash="dot"),
        showlegend=False,
        hoverinfo="skip"
    ))
    
    # Normal spending markers
    if not normal_points.empty:
        fig.add_trace(go.Scatter(
            x=normal_points["Date"],
            y=normal_points["Cost_Display"],
            mode="markers",
            name="Normal Spend",
            marker=dict(
                size=8,
                color="#60a5fa",
                line=dict(color="rgba(255, 255, 255, 0.3)", width=1)
            ),
            hovertemplate=f"<b>Normal Spend</b><br>Date: %{{x|%Y-%m-%d}}<br>Cost: {symbol}%{{y:,.2f}}<extra></extra>"
        ))
        
    # Anomaly markers (prominent, glowing red/pink)
    if not anomaly_points.empty:
        fig.add_trace(go.Scatter(
            x=anomaly_points["Date"],
            y=anomaly_points["Cost_Display"],
            mode="markers",
            name="Anomaly Detected",
            marker=dict(
                size=14,
                color="#f87171",
                symbol="diamond",
                line=dict(color="#ffffff", width=2)
            ),
            hovertemplate=f"<b>ANOMALY DETECTED</b><br>Date: %{{x|%Y-%m-%d}}<br>Cost: {symbol}%{{y:,.2f}}<extra></extra>"
        ))
        
    # Calculate sensible Y range
    max_cost = df["Cost_Display"].max() if not df.empty else 100 * rate
    y_max = max_cost * 1.15
    
    fig.update_layout(
        **CHART_LAYOUT,
        height=360,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#f1f2ff", size=11)
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            tickformat="%b %Y",
            tickfont=dict(color="#a5a8c8", size=11)
        ),
        yaxis=dict(
            tickprefix=symbol,
            range=[0, y_max],
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#a5a8c8", size=11)
        )
    )
    return fig

def create_service_trend_chart(filtered_df: pd.DataFrame, service_name: str, symbol: str = "$", rate: float = 1.0) -> go.Figure:
    """
    Builds a mini trend bar/line for the individual service explorer.
    Supports currency scaling and custom currency symbol.
    """
    df = filtered_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    monthly = df.groupby(df["Date"].dt.strftime("%Y-%m"))["Cost_USD"].sum().reset_index()
    monthly["Cost_Display"] = monthly["Cost_USD"] * rate
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["Date"],
        y=monthly["Cost_Display"],
        marker=dict(
            color="rgba(139, 92, 246, 0.8)",
            line=dict(color="#c084fc", width=1),
            cornerradius=6
        ),
        hovertemplate=f"<b>%{{x}}</b><br>Cost: {symbol}%{{y:,.2f}}<extra></extra>"
    ))
    
    layout_kwargs = dict(CHART_LAYOUT)
    layout_kwargs.update(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#a5a8c8")),
        yaxis=dict(tickprefix=symbol, gridcolor="rgba(255, 255, 255, 0.05)", tickfont=dict(size=10, color="#a5a8c8"))
    )
    fig.update_layout(**layout_kwargs)
    return fig
