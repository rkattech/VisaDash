import streamlit as st
import plotly.graph_objects as go
from charts import ChartGenerator

def render(data_generator, filters):
    st.title("📊 Executive Summary")
    
    # Get KPI data
    kpi_data = data_generator.kpi_data
    chart_gen = ChartGenerator()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Revenue (Q3 FY2025)",
            value=f"${kpi_data['current_revenue']:.1f}B",
            delta=f"{kpi_data['volume_growth']:.1f}% YoY"
        )
    
    with col2:
        st.metric(
            label="Achieved CAGR",
            value=f"{kpi_data['achieved_cagr']:.1f}%",
            delta=f"{kpi_data['achieved_cagr'] - kpi_data['target_cagr']:.1f}% vs Target"
        )
    
    with col3:
        st.metric(
            label="Market Share",
            value=f"{kpi_data['market_share']:.1f}%",
            delta="2.1% vs Prior Year"
        )
    
    with col4:
        st.metric(
            label="Revenue Yield",
            value=f"{kpi_data['revenue_yield']:.2f}%",
            delta="0.01% vs Target"
        )
    
    st.markdown("---")
    
    # KPI Gauges
    st.subheader("Performance Scorecard")
    
    gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
    
    with gauge_col1:
        cagr_gauge = chart_gen.create_kpi_gauge(
            value=kpi_data['achieved_cagr'],
            target=kpi_data['target_cagr'],
            title="CAGR Progress",
            suffix="%"
        )
        st.plotly_chart(cagr_gauge, use_container_width=True)
    
    with gauge_col2:
        revenue_gauge = chart_gen.create_kpi_gauge(
            value=kpi_data['current_revenue'],
            target=4.0,  # Q3 target
            title="Q3 Revenue",
            suffix="B"
        )
        st.plotly_chart(revenue_gauge, use_container_width=True)
    
    with gauge_col3:
        volume_gauge = chart_gen.create_kpi_gauge(
            value=kpi_data['volume_growth'],
            target=15.0,  # Volume growth target
            title="Volume Growth",
            suffix="%"
        )
        st.plotly_chart(volume_gauge, use_container_width=True)
    
    # Revenue trajectory chart
    st.subheader("Revenue Trajectory to 2030 Target")
    
    filtered_revenue_data = data_generator.get_filtered_data(data_generator.revenue_data, filters)
    revenue_trend = chart_gen.create_revenue_trend(filtered_revenue_data)
    st.plotly_chart(revenue_trend, use_container_width=True)
    
    # Progress summary
    st.subheader("Path to $22.5B by 2030")
    
    progress_col1, progress_col2 = st.columns(2)
    
    with progress_col1:
        current_progress = (kpi_data['current_revenue'] * 4 - kpi_data['base_revenue_2024']) / (kpi_data['target_revenue_2030'] - kpi_data['base_revenue_2024']) * 100
        
        st.info(f"""
        **Current Progress: {current_progress:.1f}%**
        
        - Base FY2024: ${kpi_data['base_revenue_2024']:.1f}B
        - Current Run Rate: ${kpi_data['current_revenue'] * 4:.1f}B
        - 2030 Target: ${kpi_data['target_revenue_2030']:.1f}B
        - Required CAGR: {kpi_data['target_cagr']:.1f}%
        """)
    
    with progress_col2:
        if kpi_data['achieved_cagr'] >= kpi_data['target_cagr']:
            st.success("✅ **ON TRACK** - Achieving target CAGR")
        elif kpi_data['achieved_cagr'] >= kpi_data['target_cagr'] * 0.9:
            st.warning("⚠️ **MONITOR** - Slightly below target")
        else:
            st.error("🚨 **ACTION REQUIRED** - Significantly below target")
        
        st.write(f"""
        **Key Growth Drivers:**
        - Travel recovery: +15% YoY
        - E-commerce expansion: +10% YoY  
        - B2B digitization: +8% YoY
        - New market penetration: +18% in APAC
        """)
    
    # Alerts and notifications
    if kpi_data['volume_growth'] < 12:
        st.error("🚨 **ALERT**: Volume growth below 12% threshold")
    
    if kpi_data['revenue_yield'] < 0.11:
        st.warning("⚠️ **NOTICE**: Revenue yield below optimal range")
