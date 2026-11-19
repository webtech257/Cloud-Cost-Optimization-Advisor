"""
Reusable UI Components for Cloud Cost Optimization Advisor.
Safe, un-indented rendering for Hero, Sidebar Navigation, Section Headers, and Footer.
"""

import streamlit as st
import textwrap
from ui.icons import get_icon, ICONS

def render_hero_header():
    """Renders the glass hero banner with gradient typography and tech chips."""
    graphic_svg = ICONS.get("hero_graphic", "")
    cloud_icon = get_icon("cloud")
    forecast_icon = get_icon("forecast")
    alert_icon = get_icon("alert")
    shield_icon = get_icon("shield_check")
    
    html = f"""<div class="hero-banner">
<div class="hero-content">
<div class="hero-title">Cloud Cost Optimization Advisor</div>
<div class="hero-subtitle">Intelligent AWS Cost Analysis and Forecasting</div>
<div class="hero-description">
Monitor cloud spending, predict future expenses, and discover automated cost-saving opportunities through machine learning.
</div>
<div class="hero-chips">
<span class="chip">{cloud_icon} Cloud Platform: AWS</span>
<span class="chip">{forecast_icon} Prophet ML Forecasting</span>
<span class="chip">{alert_icon} Anomaly Detection</span>
<span class="chip">{shield_icon} FinOps Analytics</span>
</div>
</div>
<div class="hero-graphic-wrap">
{graphic_svg}
</div>
</div>"""
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def render_sidebar():
    """Renders the dark glass sidebar with navigation anchors, tech badges, and ML status."""
    logo_svg = ICONS.get("logo_cloud", "")
    
    html = f"""<div style="padding: 0.5rem 0.2rem 1rem 0.2rem;">
<div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
{logo_svg}
<div>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 700; background: linear-gradient(135deg, #ffffff 40%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
Cloud Cost Advisor
</div>
<div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 500;">
Machine Learning Based AWS Cost Analysis
</div>
</div>
</div>
</div>

<div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin: 0.5rem 0 0.4rem 0.3rem;">
Dashboard Navigation
</div>

<div class="nav-group">
<a class="nav-link" href="#cost-overview">{get_icon("wallet")} Cost Overview</a>
<a class="nav-link" href="#service-costs">{get_icon("bar_chart")} Service Costs</a>
<a class="nav-link" href="#cost-trend">{get_icon("trending_up")} Monthly Trend</a>
<a class="nav-link" href="#cost-forecast">{get_icon("forecast")} Prophet Forecast</a>
<a class="nav-link" href="#recommendations">{get_icon("recommend")} Recommendations</a>
<a class="nav-link" href="#service-explorer">{get_icon("explorer")} Service Explorer</a>
<a class="nav-link" href="#download-report">{get_icon("download")} Export Report</a>
<a class="nav-link" href="#anomaly-detection">{get_icon("alert")} Anomaly Detection</a>
<a class="nav-link" href="#model-evaluation">{get_icon("shield_check")} Model Evaluation</a>
</div>

<div style="height: 1px; background: rgba(167, 139, 250, 0.15); margin: 1.25rem 0;"></div>

<div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 0.5rem; padding-left: 0.3rem;">
Tech Stack
</div>

<div class="tech-badge-container">
<span class="tech-badge">AWS Cloud</span>
<span class="tech-badge">Python 3.12</span>
<span class="tech-badge">Pandas</span>
<span class="tech-badge">Prophet ML</span>
<span class="tech-badge">Isolation Forest</span>
<span class="tech-badge">Streamlit</span>
<span class="tech-badge">Plotly 7.1</span>
</div>

<div style="height: 1px; background: rgba(167, 139, 250, 0.15); margin: 1.25rem 0;"></div>

<div class="ml-status-card">
<div class="status-indicator">
<span class="status-dot"></span>
<span>ML Engine Active</span>
</div>
<div>
This project analyzes AWS spending, forecasts future costs and suggests potential optimization strategies.
</div>
</div>"""
    st.sidebar.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def render_section_header(title: str, subtitle: str = None, icon_name: str = "cloud", anchor_id: str = None):
    """Renders a section header with anchor for smooth scrolling."""
    anchor_tag = f'<div id="{anchor_id}" style="position: relative; top: -20px; visibility: hidden;"></div>' if anchor_id else ""
    icon_svg = get_icon(icon_name)
    sub_tag = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    
    html = f"""{anchor_tag}
<div class="section-header-wrap">
<div class="section-title">
<span style="color: #c084fc; display: flex; align-items: center;">{icon_svg}</span>
<span>{title}</span>
</div>
{sub_tag}
</div>"""
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

def render_footer():
    """Renders the sleek dark SaaS footer."""
    cloud_icon = get_icon("cloud")
    html = f"""<div class="glass-footer">
<div class="footer-divider"></div>
<div style="display: flex; justify-content: center; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem; font-weight: 600; color: #f1f2ff;">
{cloud_icon} Cloud Cost Optimization Advisor
</div>
<div style="color: var(--text-muted); font-size: 0.78rem; margin-bottom: 0.25rem;">
Built with Python • AWS • Pandas • Prophet ML • Streamlit • Plotly
</div>
<div style="color: rgba(107, 111, 147, 0.7); font-size: 0.74rem;">
Academic Project | 2026
</div>
</div>"""
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
