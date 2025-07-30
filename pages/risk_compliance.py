import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from charts import ChartGenerator

def render(data_generator, filters):
    st.title("⚠️ Risk & Compliance Dashboard")
    
    chart_gen = ChartGenerator()
    risk_data = data_generator.risk_data
    
    # Risk overview metrics
    st.subheader("Risk Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if risk_data['fraud_rate'] < 0.5:
            st.metric("Fraud Rate", f"{risk_data['fraud_rate']:.2f}%", "✅ Below Target", delta_color="inverse")
        else:
            st.metric("Fraud Rate", f"{risk_data['fraud_rate']:.2f}%", "🚨 Above Target", delta_color="normal")
    
    with col2:
        if risk_data['chargeback_ratio'] < 1.0:
            st.metric("Chargeback Ratio", f"{risk_data['chargeback_ratio']:.1f}%", "✅ Below Target", delta_color="inverse")
        else:
            st.metric("Chargeback Ratio", f"{risk_data['chargeback_ratio']:.1f}%", "🚨 Above Target", delta_color="normal")
    
    with col3:
        if risk_data['compliance_score'] >= 90:
            st.metric("Compliance Score", f"{risk_data['compliance_score']:.0f}%", "✅ Above Target")
        else:
            st.metric("Compliance Score", f"{risk_data['compliance_score']:.0f}%", "⚠️ Below Target")
    
    with col4:
        if risk_data['uptime_pct'] >= 99.9:
            st.metric("System Uptime", f"{risk_data['uptime_pct']:.2f}%", "✅ Above Target")
        else:
            st.metric("System Uptime", f"{risk_data['uptime_pct']:.2f}%", "⚠️ Below Target")
    
    # Risk dashboard with gauges
    st.subheader("Risk Metrics Dashboard")
    risk_dashboard = chart_gen.create_risk_dashboard(risk_data)
    st.plotly_chart(risk_dashboard, use_container_width=True)
    
    # Risk incident heatmap
    st.subheader("Risk Incident Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mock incident data by type and severity
        incident_data = {
            'Incident Type': ['Fraud Attempt', 'System Outage', 'Data Breach', 'Compliance Violation', 'Operational Error'] * 4,
            'Severity': ['Critical', 'High', 'Medium', 'Low'] * 5,
            'Count': [2, 5, 12, 8, 0, 3, 8, 15, 1, 1, 6, 20, 0, 2, 10, 25, 1, 0, 5, 18]
        }
        
        # Create pivot table for heatmap
        import pandas as pd
        incident_df = pd.DataFrame(incident_data)
        heatmap_data = incident_df.pivot_table(values='Count', index='Incident Type', columns='Severity', fill_value=0)
        
        fig = px.imshow(heatmap_data.values,
                       labels=dict(x="Severity", y="Incident Type", color="Count"),
                       x=heatmap_data.columns,
                       y=heatmap_data.index,
                       color_continuous_scale='Reds',
                       title="Risk Incident Heatmap (Last 90 Days)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk trend over time
        import numpy as np
        
        months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
        fraud_rates = [0.42, 0.38, 0.45, 0.41, 0.39, 0.43, 0.45]
        compliance_scores = [94, 95, 93, 96, 95, 94, 95]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=fraud_rates, mode='lines+markers', 
                                name='Fraud Rate (%)', yaxis='y'))
        fig.add_trace(go.Scatter(x=months, y=compliance_scores, mode='lines+markers',
                                name='Compliance Score (%)', yaxis='y2'))
        
        fig.update_layout(
            title="Risk Metrics Trend (7 Months)",
            yaxis=dict(title="Fraud Rate (%)", side="left"),
            yaxis2=dict(title="Compliance Score (%)", side="right", overlaying="y"),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Regulatory compliance section
    st.subheader("Regulatory Compliance Status")
    
    tab1, tab2, tab3 = st.tabs(["AML/KYC", "Data Privacy", "Financial Regulations"])
    
    with tab1:
        st.write("**Anti-Money Laundering & Know Your Customer**")
        
        aml_col1, aml_col2 = st.columns(2)
        
        with aml_col1:
            st.info(f"""
            **AML Metrics:**
            - Active Alerts: {risk_data['aml_alerts']}
            - False Positive Rate: 12%
            - Investigation Time: 3.2 days avg
            - Regulatory Reports Filed: 156
            """)
        
        with aml_col2:
            # AML alert trends
            alert_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
            alert_counts = [28, 31, 25, 29, 23, 26, 23]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=alert_months, y=alert_counts, 
                               marker_color='orange', name='AML Alerts'))
            fig.add_hline(y=30, line_dash="dash", line_color="red",
                         annotation_text="Alert Threshold")
            fig.update_layout(title="Monthly AML Alerts", height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.write("**Data Privacy & Protection**")
        
        privacy_metrics = {
            'Metric': ['GDPR Compliance', 'Data Breach Incidents', 'Privacy Impact Assessments', 'Data Subject Requests', 'Consent Management'],
            'Status': ['✅ Compliant', '✅ 0 incidents', '✅ 12 completed', '⚠️ 45 pending', '✅ 99.2% coverage'],
            'Target': ['100%', '0', '12/quarter', '<30 days', '>95%'],
            'Current': ['98.5%', '0', '12', '28 days avg', '99.2%']
        }
        
        st.dataframe(privacy_metrics, use_container_width=True, hide_index=True)
    
    with tab3:
        st.write("**Financial Services Regulations**")
        
        reg_col1, reg_col2 = st.columns(2)
        
        with reg_col1:
            st.success("""
            **Compliant Jurisdictions:**
            ✅ United States (Fed, OCC, CFPB)
            ✅ European Union (PSD2, MiFID II)
            ✅ United Kingdom (FCA)
            ✅ Singapore (MAS)
            ✅ Australia (ASIC)
            """)
        
        with reg_col2:
            st.warning("""
            **Regulatory Changes Monitoring:**
            ⚠️ New CBDC regulations (EU) - Q2 2025
            ⚠️ Enhanced sanctions screening (US) - Q1 2025
            ⚠️ Open banking updates (UK) - Q3 2025
            ⚠️ Consumer protection rules (LATAM) - Q4 2025
            """)
    
    # FSB (Financial Stability Board) KPIs
    st.subheader("FSB Cross-Border Payment KPIs")
    
    fsb_col1, fsb_col2, fsb_col3, fsb_col4 = st.columns(4)
    
    with fsb_col1:
        st.metric("Transaction Cost", f"{risk_data['transaction_cost']:.1f}%", "✅ Below 1% target")
    
    with fsb_col2:
        st.metric("Settlement Speed", "< 1 hour", "✅ 80% of transactions")
    
    with fsb_col3:
        st.metric("Transparency Score", "85/100", "⚠️ Target: 90")
    
    with fsb_col4:
        st.metric("Access Coverage", "78%", "⚠️ Target: 85%")
    
    # Risk alerts and actions
    st.subheader("Active Risk Alerts & Actions")
    
    alerts = [
        {"type": "High", "message": "Fraud rate approaching 0.5% threshold in APAC region", "action": "Enhanced monitoring deployed"},
        {"type": "Medium", "message": "Compliance audit scheduled for Q2 2025", "action": "Preparation team assigned"},
        {"type": "Low", "message": "System latency increased by 5ms average", "action": "Performance team investigating"},
        {"type": "Medium", "message": "New AML regulation effective March 2025", "action": "Policy update in progress"}
    ]
    
    for alert in alerts:
        if alert["type"] == "High":
            st.error(f"🚨 **{alert['type']} Risk**: {alert['message']}\n\n**Action**: {alert['action']}")
        elif alert["type"] == "Medium":
            st.warning(f"⚠️ **{alert['type']} Risk**: {alert['message']}\n\n**Action**: {alert['action']}")
        else:
            st.info(f"ℹ️ **{alert['type']} Risk**: {alert['message']}\n\n**Action**: {alert['action']}")
