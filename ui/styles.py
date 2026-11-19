"""
Design System and Global CSS Injection for Cloud Cost Optimization Advisor.
Dark glassmorphism, responsive grid, typography, and Streamlit element overrides.
"""

import streamlit as st
import textwrap

CSS_THEME = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg-0: #05060f;
    --bg-1: #0a0b1e;
    --bg-2: #11122b;
    --violet: #8b5cf6;
    --purple: #a855f7;
    --electric-blue: #3b82f6;
    --cyan-accent: #22d3ee;
    --text-primary: #f1f2ff;
    --text-secondary: #a5a8c8;
    --text-muted: #6b6f93;
    --success: #34d399;
    --warning: #fbbf24;
    --danger: #f87171;
    --glass-bg: rgba(255, 255, 255, 0.035);
    --glass-bg-hover: rgba(255, 255, 255, 0.06);
    --glass-border: rgba(167, 139, 250, 0.18);
    --glass-border-hover: rgba(167, 139, 250, 0.38);
    --glow: 0 0 24px rgba(139, 92, 246, 0.35);
}

/* Global resets & typography */
html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--text-primary);
    scroll-behavior: smooth;
    scroll-padding-top: 80px;
}

/* Protect Streamlit Material Symbols & Icons from font-family override */
[data-testid="stIconMaterial"], 
[data-testid="stExpanderToggleIcon"],
span[data-testid="stIconMaterial"],
i, 
.material-symbols-rounded, 
.material-symbols-outlined {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
}

h1, h2, h3, .font-heading {
    font-family: 'Space Grotesk', -apple-system, sans-serif;
    letter-spacing: -0.02em;
}

/* App Background: Layered Radial Gradients & Network Pattern */
.stApp {
    background: 
        radial-gradient(circle at 85% 8%, rgba(139, 92, 246, 0.14) 0%, transparent 45%),
        radial-gradient(circle at 15% 92%, rgba(59, 130, 246, 0.12) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.04) 0%, transparent 60%),
        linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 100%) !important;
    background-attachment: fixed !important;
}

/* Subtle background grid pattern */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: radial-gradient(rgba(139, 92, 246, 0.10) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}

/* Container constraints */
.block-container {
    max-width: 1320px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    position: relative;
    z-index: 1;
}

/* Header & toolbar adjustments */
header[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: none !important;
}
#MainMenu, footer {
    visibility: hidden;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(5, 6, 15, 0.6);
}
::-webkit-scrollbar-thumb {
    background: rgba(139, 92, 246, 0.3);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(139, 92, 246, 0.6);
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10, 11, 30, 0.95) 0%, rgba(5, 6, 15, 0.98) 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(20px) !important;
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(167, 139, 250, 0.12) !important;
    margin: 1.25rem 0 !important;
}

/* Base Glassmorphism Card */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(16px) saturate(140%);
    -webkit-backdrop-filter: blur(16px) saturate(140%);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    transition: all 250ms cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}
.glass-card:hover {
    transform: translateY(-4px);
    border-color: var(--glass-border-hover);
    box-shadow: 0 14px 44px rgba(0, 0, 0, 0.55), 0 0 24px rgba(139, 92, 246, 0.22);
}

/* Gradient Dividers */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent 0%, rgba(139, 92, 246, 0.35) 50%, transparent 100%) !important;
    margin: 2.2rem 0 !important;
}

/* Native Streamlit Metric Card Dark Glassmorphism Styling */
div[data-testid="stMetric"] {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(16px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(16px) saturate(140%) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 18px !important;
    padding: 1.25rem 1.4rem !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    transition: all 250ms ease !important;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    border-color: var(--glass-border-hover) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55), 0 0 20px rgba(139, 92, 246, 0.22) !important;
}
div[data-testid="stMetricLabel"] p {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--text-muted) !important;
}
div[data-testid="stMetricValue"] div {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-variant-numeric: tabular-nums !important;
}
div[data-testid="stMetricDelta"] {
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: #34d399 !important; /* Vibrant emerald green for positive savings/cost reduction */
}

/* Streamlit Native Alert Restyling */
div[data-testid="stAlert"] {
    background: rgba(17, 18, 43, 0.65) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    color: var(--text-primary) !important;
    padding: 0.9rem 1.2rem !important;
    margin-bottom: 1rem !important;
}

/* Hero Banner */
.hero-banner {
    padding: 2.25rem 2.5rem;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.045) 0%, rgba(139, 92, 246, 0.06) 100%);
    border: 1px solid var(--glass-border);
    position: relative;
    border-radius: 20px;
}
.hero-content {
    max-width: 680px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.15;
    background: linear-gradient(135deg, #ffffff 30%, #c084fc 70%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.6rem;
}
.hero-subtitle {
    font-size: 1.15rem;
    font-weight: 500;
    color: #c084fc;
    margin-bottom: 0.6rem;
}
.hero-description {
    font-size: 0.92rem;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 1.25rem;
}
.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
}
.chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(167, 139, 250, 0.2);
    color: var(--text-secondary);
}

/* Sidebar Nav Pills */
.nav-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin-bottom: 1rem;
}
.nav-link {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.6rem 0.85rem;
    border-radius: 12px;
    color: var(--text-secondary);
    text-decoration: none !important;
    font-size: 0.86rem;
    font-weight: 500;
    transition: all 200ms ease;
    border: 1px solid transparent;
}
.nav-link:hover {
    color: #ffffff;
    background: rgba(139, 92, 246, 0.12);
    border-color: rgba(139, 92, 246, 0.25);
    transform: translateX(3px);
}

/* Sidebar Tech Stack Badges */
.tech-badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.5rem;
}
.tech-badge {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.25rem 0.55rem;
    border-radius: 8px;
    background: rgba(17, 18, 43, 0.8);
    border: 1px solid rgba(167, 139, 250, 0.18);
    color: var(--text-secondary);
}

/* Sidebar ML Status Card */
.ml-status-card {
    padding: 0.9rem;
    border-radius: 14px;
    background: rgba(17, 18, 43, 0.6);
    border-left: 3px solid var(--violet);
    border-top: 1px solid rgba(167, 139, 250, 0.15);
    border-right: 1px solid rgba(167, 139, 250, 0.15);
    border-bottom: 1px solid rgba(167, 139, 250, 0.15);
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.45;
}
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.35rem;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 10px #34d399;
    animation: pulse-glow 2s infinite;
}
@keyframes pulse-glow {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.9); }
}

/* Section Header styling */
.section-header-wrap {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    scroll-margin-top: 80px;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.25rem;
}
.section-subtitle {
    font-size: 0.88rem;
    color: var(--text-secondary);
    margin-left: 0.2rem;
}

/* Radio Group Pill Styling */
div[data-testid="stRadio"] > div {
    gap: 0.65rem !important;
}
div[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    padding: 0.45rem 1rem !important;
    cursor: pointer !important;
    transition: all 200ms ease !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: var(--violet) !important;
    background: rgba(139, 92, 246, 0.12) !important;
}
div[data-testid="stRadio"] label span {
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
}

/* Streamlit Selectbox Override */
div[data-baseweb="select"] {
    background-color: rgba(17, 18, 43, 0.7) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="select"]:hover {
    border-color: var(--violet) !important;
}
div[data-baseweb="popover"] ul {
    background-color: #0a0b1e !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}

/* Streamlit Download Button Override */
div[data-testid="stDownloadButton"] button, div[data-testid="stBaseButton-secondary"] button {
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 14px !important;
    padding: 0.65rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.35) !important;
    transition: all 250ms ease !important;
}
div[data-testid="stDownloadButton"] button:hover, div[data-testid="stBaseButton-secondary"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(139, 92, 246, 0.55) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

/* Streamlit Dataframe Glass Wrapper */
div[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    border: 1px solid var(--glass-border) !important;
    overflow: hidden !important;
    background: rgba(10, 11, 30, 0.4) !important;
}

/* Streamlit Expander styling */
[data-testid="stExpander"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    margin-top: 1rem !important;
}

/* Footer styling */
.glass-footer {
    padding: 2rem 1rem 1rem 1rem;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.82rem;
    margin-top: 3rem;
}
.footer-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.25), transparent);
    margin-bottom: 1.5rem;
}

/* Responsiveness */
@media (max-width: 992px) {
    .hero-banner {
        flex-direction: column;
        align-items: flex-start;
        gap: 1.5rem;
    }
    .hero-title {
        font-size: 2rem;
    }
}
@media (max-width: 640px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .hero-title {
        font-size: 1.7rem;
    }
}

/* Reduced Motion Pass */
@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
"""

def inject_css():
    """Injects the consolidated design system CSS into the Streamlit app."""
    css_wrapped = f"<style>\n{CSS_THEME.strip()}\n</style>"
    st.markdown(css_wrapped, unsafe_allow_html=True)
