import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Import page modules
from pages.executive_summary import render as executive_summary_render
from pages.performance_tracking import render as performance_tracking_render
from pages.opportunity_identification import render as opportunity_identification_render
from pages.risk_compliance import render as risk_compliance_render
from pages.forecasting import render as forecasting_render
from utils.filters import GlobalFilters
from data_generator import DataGenerator

# Visa brand colors
VISA_BLUE = "#003087"
VISA_GREEN = "#00A86B"
VISA_RED = "#E31837"

# Page configuration
st.set_page_config(
    page_title="Visa Cross-Border Analytics Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Visa branding
st.markdown(f"""
<style>
    .main-header {{
        color: {VISA_BLUE};
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid {VISA_BLUE};
        margin-bottom: 2rem;
    }}
    .metric-positive {{
        color: {VISA_GREEN};
    }}
    .metric-negative {{
        color: {VISA_RED};
    }}
    .metric-neutral {{
        color: {VISA_BLUE};
    }}
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize data generator
    if 'data_generator' not in st.session_state:
        st.session_state.data_generator = DataGenerator()
    
    # Initialize global filters
    if 'global_filters' not in st.session_state:
        st.session_state.global_filters = GlobalFilters()
    
    # Main header
    st.markdown('<h1 class="main-header">Visa Cross-Border Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    pages = {
        "📊 Executive Summary": "executive_summary",
        "📈 Performance Tracking": "performance_tracking", 
        "🎯 Opportunity Identification": "opportunity_identification",
        "⚠️ Risk & Compliance": "risk_compliance",
        "🔮 Forecasting": "forecasting"
    }
    
    selected_page = st.sidebar.selectbox("Select View", list(pages.keys()))
    
    # Global filters in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Global Filters")
    
    # Apply global filters
    filters = st.session_state.global_filters.render_filters()
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.session_state.data_generator = DataGenerator()
        st.rerun()
    
    # Export options
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Export Options")
    
    if st.sidebar.button("📄 Export PDF"):
        st.sidebar.success("PDF export functionality would be implemented here")
    
    if st.sidebar.button("📊 Export CSV"):
        st.sidebar.success("CSV export functionality would be implemented here")
    
    # Render selected page
    page_key = pages[selected_page]
    
    if page_key == "executive_summary":
        executive_summary_render(st.session_state.data_generator, filters)
    elif page_key == "performance_tracking":
        performance_tracking_render(st.session_state.data_generator, filters)
    elif page_key == "opportunity_identification":
        opportunity_identification_render(st.session_state.data_generator, filters)
    elif page_key == "risk_compliance":
        risk_compliance_render(st.session_state.data_generator, filters)
    elif page_key == "forecasting":
        forecasting_render(st.session_state.data_generator, filters)

if __name__ == "__main__":
    main()
