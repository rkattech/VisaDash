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

def render_floating_chatbot():
    """Render floating chat bubble and chat window using Streamlit components"""
    # Initialize chatbot states
    if 'show_chat_window' not in st.session_state:
        st.session_state.show_chat_window = False
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant", 
                "content": "Hello! I'm your Visa Analytics AI Assistant.\n\nI'm here to help you navigate and understand this cross-border business analytics dashboard. Here's what I can assist you with:\n\n• **Data Insights**: I can explain the source of any data, methodology behind calculations, and provide context for metrics and trends.\n\n• **Technical Support**: Need to report a bug or provide feedback to the development team? I can help document and route your feedback.\n\n• **Custom Exports**: Want specific views, filtered data, or custom reports? I can help create tailored exports based on your needs.\n\n• **Dashboard Navigation**: I can guide you through different sections, explain visualizations, and help you find specific information.\n\n• **Business Analysis**: Ask me about trends, performance insights, forecasting scenarios, or competitive analysis.\n\n• **Feature Requests**: Have ideas for dashboard improvements? I can collect your suggestions and communicate them to the development team.\n\nFeel free to ask me anything about the dashboard, the data, or how to get the most value from these analytics!"
            }
        ]
    
    # Add CSS for floating chat bubble
    st.markdown("""
    <style>
    .floating-chat-bubble {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #003087, #0066CC);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(0, 48, 135, 0.3);
        z-index: 1000;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .floating-chat-bubble:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(0, 48, 135, 0.4);
    }
    
    .chat-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1001;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .chat-window {
        width: 500px;
        height: 600px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .chat-window-header {
        background: linear-gradient(135deg, #003087, #0066CC);
        color: white;
        padding: 20px;
        font-weight: bold;
        font-size: 18px;
    }
    
    .chat-messages-area {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        background: #f8f9fa;
    }
    
    .message {
        margin-bottom: 15px;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: #003087;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        border: 1px solid #e0e0e0;
        border-bottom-left-radius: 5px;
        white-space: pre-line;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render floating chat bubble button using HTML
    st.markdown("""
    <div class="floating-chat-bubble" onclick="document.getElementById('chat_bubble_btn').click()">
        💬
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button that gets triggered by the HTML bubble
    if st.button("", key="chat_bubble_btn", help="Toggle Chat"):
        st.session_state.show_chat_window = not st.session_state.show_chat_window
        st.rerun()
    
    # Chat window modal overlay
    if st.session_state.show_chat_window:
        # Create modal-like overlay
        with st.container():
            # Header
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown("### 💬 AI Assistant")
            with col2:
                if st.button("✕", key="close_chat_window"):
                    st.session_state.show_chat_window = False
                    st.rerun()
            
            st.markdown("---")
            
            # Messages display area with custom styling
            with st.container():
                st.markdown('<div style="height: 400px; overflow-y: auto; padding: 10px; background: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
                
                for message in st.session_state.chat_messages:
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div style="text-align: right; margin: 10px 0;">
                            <div style="display: inline-block; background: #003087; color: white; padding: 10px 15px; border-radius: 15px 15px 5px 15px; max-width: 70%;">
                                {message["content"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="text-align: left; margin: 10px 0;">
                            <div style="display: inline-block; background: white; color: #333; padding: 10px 15px; border-radius: 15px 15px 15px 5px; border: 1px solid #e0e0e0; max-width: 70%; white-space: pre-line;">
                                {message["content"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat input area
            user_input = st.text_area("Ask me anything about the dashboard:", 
                                    key="chat_input", 
                                    height=100,
                                    placeholder="e.g., What's the source of the revenue data? Can you create a custom export for Q3 metrics?")
            
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("Send", key="send_message", type="primary"):
                    if user_input.strip():
                        # Add user message
                        st.session_state.chat_messages.append({"role": "user", "content": user_input})
                        
                        # Generate AI response
                        ai_response = generate_ai_response(user_input)
                        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                        
                        st.rerun()

def generate_ai_response(user_input):
    """Generate AI response based on user input"""
    user_input_lower = user_input.lower()
    
    # Data source questions
    if any(word in user_input_lower for word in ['data', 'source', 'where', 'from']):
        return """📊 **Data Sources Information**

The dashboard uses synthetic data generated for demonstration purposes. Here are the key data sources:

• **Revenue Data**: Mock quarterly data from FY2024-Q4 to FY2025, simulating realistic growth patterns
• **Geographic Data**: Simulated performance across 25 countries in 5 regions
• **Product Metrics**: Generated data for Visa Direct, B2B Connect, Traditional Cards, and Other Services
• **Risk Metrics**: Synthetic compliance, fraud, and operational risk indicators
• **Forecasting**: Monte Carlo simulations based on industry benchmarks

For production use, this would integrate with live Visa data systems, payment networks, and external market data providers."""
    
    # Export questions
    elif any(word in user_input_lower for word in ['export', 'download', 'report', 'csv', 'pdf']):
        return """📄 **Custom Export Options**

I can help you create custom exports tailored to your needs:

**Available Export Formats:**
• CSV data files for specific metrics or time periods
• PDF reports with selected visualizations
• Excel workbooks with multiple data sheets
• PowerPoint-ready charts and summaries

**Custom Export Examples:**
• Q3 FY2025 performance metrics only
• Geographic analysis for specific regions
• Risk dashboard summary for compliance reporting
• Forecasting scenarios for executive presentations

To request a custom export, just tell me:
1. Which sections/metrics you need
2. Time period or filters to apply
3. Preferred format (CSV, PDF, Excel, etc.)

*Note: In this demo, export functionality is simulated. Production version would generate actual files.*"""
    
    # Feedback questions
    elif any(word in user_input_lower for word in ['feedback', 'bug', 'issue', 'problem', 'suggestion']):
        return """🛠️ **Feedback & Support**

I'm here to collect your feedback and route it to the development team:

**Types of Feedback:**
• Bug reports or technical issues
• Feature requests or improvements
• Data accuracy concerns
• UI/UX suggestions
• Performance issues

**How to Submit Feedback:**
1. Describe the issue or suggestion clearly
2. Include specific steps to reproduce (for bugs)
3. Mention which dashboard section is affected
4. Suggest your preferred solution (if any)

I'll document your feedback with relevant details and ensure it reaches the development team with appropriate priority.

**Common Issues:**
• Chart loading slowly → Clear browser cache
• Filters not working → Try refreshing the page
• Data not updating → Use the "Refresh Data" button

What specific feedback would you like to share?"""
    
    # Navigation help
    elif any(word in user_input_lower for word in ['navigate', 'section', 'find', 'where', 'how']):
        return """🧭 **Dashboard Navigation Guide**

**Main Sections:**
📊 **Executive Summary** - High-level KPIs, revenue trajectory, progress tracking
📈 **Performance Tracking** - Detailed revenue/volume trends, geographic breakdown, product analysis
🎯 **Opportunity Identification** - Market opportunities, competitive analysis, partnerships
⚠️ **Risk & Compliance** - Risk metrics, regulatory status, incident monitoring
🔮 **Forecasting** - Scenario planning, Monte Carlo simulation, sensitivity analysis

**Navigation Tips:**
• Use the radio buttons in the left sidebar to switch between sections
• Click "Filters" in the top-right to customize data views
• Each section has tabs for different sub-analyses
• Hover over charts for detailed tooltips
• Use the refresh button to reload data

**Finding Specific Information:**
• Revenue targets → Executive Summary
• Geographic performance → Performance Tracking > Geographic tab
• Market opportunities → Opportunity Identification > Market Opportunities
• Risk status → Risk & Compliance
• Future projections → Forecasting

What specific information are you looking for?"""
    
    # Business analysis questions
    elif any(word in user_input_lower for word in ['analysis', 'trend', 'performance', 'forecast', 'growth']):
        return """📈 **Business Analysis Insights**

**Current Performance Highlights:**
• Revenue: $3.5B in Q3 FY2025 (13% YoY growth)
• CAGR: 9.5% achieved vs 10% target
• Market Share: 22% globally
• Volume Growth: 13% YoY (above 12% threshold)

**Key Trends:**
• Asia-Pacific leading growth at 18%
• B2B digitization driving 25% growth in B2B Connect
• Travel recovery contributing 15% YoY increase
• Risk metrics remain within acceptable ranges

**Strategic Insights:**
• On track for 2030 target with current trajectory
• Untapped opportunities in emerging corridors
• Competitive position strong but innovation gap exists
• Regulatory environment generally supportive

**Areas for Focus:**
• Accelerate partnership acquisitions
• Improve cost competitiveness vs fintechs
• Enhance B2B penetration in key markets
• Monitor regulatory changes in EU and APAC

Would you like me to dive deeper into any specific metric or trend?"""
    
    # Default response
    else:
        return f"""🤖 **I'm here to help!**

I see you asked: "{user_input}"

I can assist you with:
• **Data questions** - Sources, methodologies, calculations
• **Export requests** - Custom reports, filtered data, specific formats
• **Technical support** - Bug reports, feedback, feature requests
• **Navigation help** - Finding information, using features
• **Business insights** - Trends, performance analysis, forecasts

Could you please be more specific about what you'd like to know? For example:
• "What's the source of the revenue data?"
• "Can you export Q3 performance metrics?"
• "How do I find competitive analysis?"
• "What's driving the growth in Asia-Pacific?"

I'm ready to provide detailed assistance with any aspect of the dashboard!"""

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
    
    # Render floating chatbot
    render_floating_chatbot()
    
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
