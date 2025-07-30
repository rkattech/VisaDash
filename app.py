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

# Hide Streamlit's default navigation
hide_streamlit_style = """
<style>
/* Hide Streamlit's auto-generated page navigation */
section[data-testid="stSidebar"] > div:first-child > div:first-child {display: none}
section[data-testid="stSidebar"] .css-ng1t4o {display: none}
section[data-testid="stSidebar"] .css-1d391kg {display: none}
section[data-testid="stSidebar"] nav[aria-label="Page navigation"] {display: none}
section[data-testid="stSidebar"] div[role="navigation"] {display: none}
ul[role="tablist"] {display: none}
div[data-testid="stSidebarNav"] {display: none}
nav[data-testid="stSidebarNav"] {display: none}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS for Visa branding and filters overlay
st.markdown(f"""
<style>
    .main-header {{
        color: {VISA_BLUE};
        text-align: left;
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
    
    /* Navigation radio buttons styling */
    .stRadio > div[role="radiogroup"] > label {{
        background: transparent;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }}
    .stRadio > div[role="radiogroup"] > label:hover {{
        background-color: {VISA_BLUE};
        color: white;
        border-color: {VISA_BLUE};
    }}
    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {{
        background-color: {VISA_BLUE};
        color: white;
        border-color: {VISA_BLUE};
        font-weight: bold;
    }}
    .stRadio > div[role="radiogroup"] > label > div {{
        display: flex;
        align-items: center;
    }}
    .stRadio > div[role="radiogroup"] > label > div > div:first-child {{
        margin-right: 0.5rem;
    }}
    
    /* Filters toggle button styling */
    div[data-testid="column"]:nth-child(2) .stButton > button {{
        background-color: {VISA_BLUE};
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.2s ease;
    }}
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {{
        background-color: {VISA_GREEN};
        color: white;
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
    
    # Main header with filters toggle
    header_col1, header_col2 = st.columns([5, 1])
    with header_col1:
        st.markdown('<h1 class="main-header">Visa Cross-Border Analytics Dashboard</h1>', unsafe_allow_html=True)
    with header_col2:
        # Initialize filters visibility state
        if 'show_filters' not in st.session_state:
            st.session_state.show_filters = False
        
        if st.button("🔍 Filters", key="filters_toggle", help="Show/Hide Filters"):
            st.session_state.show_filters = not st.session_state.show_filters
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    pages = {
        "📊 Executive Summary": "executive_summary",
        "📈 Performance Tracking": "performance_tracking", 
        "🎯 Opportunity Identification": "opportunity_identification",
        "⚠️ Risk & Compliance": "risk_compliance",
        "🔮 Forecasting": "forecasting"
    }
    
    # Initialize selected page in session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "📊 Executive Summary"
    
    # Create navigation menu as radio buttons for better UX
    page_names = list(pages.keys())
    current_index = page_names.index(st.session_state.selected_page) if st.session_state.selected_page in page_names else 0
    
    selected_page = st.sidebar.radio(
        "Views",
        page_names,
        index=current_index,
        key="navigation_radio",
        label_visibility="hidden"
    )
    
    # Update session state if selection changed
    if selected_page != st.session_state.selected_page:
        st.session_state.selected_page = selected_page
    
    # Filters panel (conditionally shown)
    if st.session_state.show_filters:
        with st.expander("🔍 Dashboard Filters", expanded=True):
            filters = st.session_state.global_filters.render_filters()
    else:
        # Use default filters when panel is hidden
        filters = {
            'segments': ['Travel', 'E-commerce', 'B2B', 'Remittances'],
            'regions': ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa'],
            'products': ['Visa Direct', 'B2B Connect', 'Traditional Cards', 'Other Services'],
            'currency': 'USD'
        }
    
    # Data refresh button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Refresh Data"):
        st.session_state.data_generator = DataGenerator()
        st.rerun()
    
    # Export options
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
