import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from charts import ChartGenerator

def render(data_generator, filters):
    st.title("🎯 Opportunity Identification")
    
    chart_gen = ChartGenerator()
    
    # Tabs for different opportunity views
    tab1, tab2, tab3 = st.tabs(["Market Opportunities", "Competitive Analysis", "Partnership Pipeline"])
    
    with tab1:
        st.subheader("Market Opportunity Heatmap")
        
        # Market opportunity bubble chart
        opportunity_bubble = chart_gen.create_opportunity_bubble(data_generator.opportunity_data)
        st.plotly_chart(opportunity_bubble, use_container_width=True)
        
        # Opportunity ranking
        st.subheader("Top Market Opportunities")
        
        # Calculate opportunity score
        opp_data = data_generator.opportunity_data.copy()
        opp_data['opportunity_score'] = (
            opp_data['potential_revenue_b'] * 0.4 +
            opp_data['growth_potential'] * 0.3 +
            (100 - opp_data['current_penetration']) * 0.2 +
            opp_data['market_size_b'] * 0.1
        )
        
        top_opportunities = opp_data.nlargest(10, 'opportunity_score')[
            ['corridor', 'potential_revenue_b', 'current_penetration', 'growth_potential', 'visa_share', 'opportunity_score']
        ].round(2)
        
        top_opportunities.columns = [
            'Corridor', 'Potential Revenue ($B)', 'Current Penetration (%)', 
            'Growth Potential (%)', 'Visa Share (%)', 'Opportunity Score'
        ]
        
        st.dataframe(top_opportunities, use_container_width=True)
        
        # Untapped corridors analysis
        st.subheader("Untapped High-Value Corridors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Low penetration, high potential
            untapped = opp_data[
                (opp_data['current_penetration'] < 20) & 
                (opp_data['potential_revenue_b'] > 3)
            ].nlargest(5, 'potential_revenue_b')
            
            st.write("**Low Penetration, High Revenue Potential:**")
            for _, row in untapped.iterrows():
                st.write(f"• {row['corridor']}: ${row['potential_revenue_b']:.1f}B potential, {row['current_penetration']:.1f}% penetration")
        
        with col2:
            # High growth potential
            growth_opps = opp_data.nlargest(5, 'growth_potential')
            
            st.write("**Highest Growth Potential:**")
            for _, row in growth_opps.iterrows():
                st.write(f"• {row['corridor']}: {row['growth_potential']:.1f}% growth potential, {row['visa_share']:.1f}% current share")
        
        # Market trends
        st.subheader("Emerging Market Trends")
        
        trends_data = {
            'Trend': ['Digital Remittances', 'CBDC Adoption', 'B2B Digitization', 'Cross-border E-commerce', 'Crypto Integration'],
            'Growth Rate': [45, 15, 30, 25, 80],
            'Market Size ($B)': [25, 50, 100, 75, 10],
            'Visa Opportunity': ['High', 'Medium', 'High', 'High', 'Low']
        }
        
        fig = px.scatter(trends_data, x='Market Size ($B)', y='Growth Rate',
                        size=[5]*len(trends_data['Trend']), 
                        hover_name='Trend',
                        color='Visa Opportunity',
                        color_discrete_map={'High': 'green', 'Medium': 'yellow', 'Low': 'red'},
                        title="Emerging Trends Analysis")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Competitive Analysis")
        
        # Competitive positioning radar chart
        competitors = ['Visa', 'Mastercard', 'Swift', 'Western Union', 'Wise']
        metrics = ['Market Share', 'Innovation', 'Speed', 'Cost', 'Coverage', 'Brand']
        
        # Mock competitive data
        comp_data = {
            'Visa': [25, 85, 90, 75, 95, 90],
            'Mastercard': [22, 80, 85, 78, 90, 85],
            'Swift': [15, 60, 40, 60, 100, 80],
            'Western Union': [8, 50, 70, 50, 85, 75],
            'Wise': [3, 90, 95, 95, 60, 70]
        }
        
        fig = go.Figure()
        
        for competitor in competitors:
            fig.add_trace(go.Scatterpolar(
                r=comp_data[competitor],
                theta=metrics,
                fill='toself' if competitor == 'Visa' else None,
                name=competitor,
                line=dict(width=3 if competitor == 'Visa' else 2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Competitive Positioning Analysis",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Competitive insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Visa Strengths")
            st.success("""
            ✅ **Market Leadership**: 25% global share
            ✅ **Network Coverage**: 95% global reach
            ✅ **Brand Recognition**: Strongest brand equity
            ✅ **Transaction Speed**: Industry-leading processing
            """)
        
        with col2:
            st.subheader("Improvement Areas")
            st.warning("""
            ⚠️ **Cost Competitiveness**: Higher fees vs newcomers
            ⚠️ **Innovation Speed**: Slower than fintechs
            ⚠️ **Digital Native Features**: Playing catch-up
            ⚠️ **SME Penetration**: Lower than specialized players
            """)
        
        # Market share trends
        st.subheader("Market Share Trends (Last 5 Years)")
        
        years = [2020, 2021, 2022, 2023, 2024]
        share_trends = {
            'Visa': [26, 25.5, 25.2, 24.8, 25],
            'Mastercard': [20, 20.5, 21, 21.5, 22],
            'Swift': [18, 17, 16, 15.5, 15],
            'Western Union': [10, 9.5, 9, 8.5, 8],
            'Others': [26, 27.5, 28.8, 29.7, 30]
        }
        
        fig = go.Figure()
        for competitor, shares in share_trends.items():
            fig.add_trace(go.Scatter(x=years, y=shares, mode='lines+markers', name=competitor))
        
        fig.update_layout(
            title="Cross-Border Payment Market Share Evolution",
            xaxis_title="Year",
            yaxis_title="Market Share (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Partnership and Pipeline Analysis")
        
        # Partnership funnel
        funnel_data = {
            'Stage': ['Awareness', 'Interest', 'Evaluation', 'Negotiation', 'Closed'],
            'Count': [50, 25, 15, 8, 3],
            'Value ($M)': [5000, 2500, 1500, 800, 300]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Count'],
                textinfo="value+percent initial",
                marker=dict(color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
            ))
            fig.update_layout(title="Partnership Pipeline - Count", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Value ($M)'],
                textinfo="value+percent initial",
                marker=dict(color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
            ))
            fig.update_layout(title="Partnership Pipeline - Value ($M)", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Active partnerships
        st.subheader("Recent Partnership Wins")
        
        partnerships = {
            'Partner': ['Southeast Asian Bank', 'European Fintech', 'LATAM Processor', 'African Mobile Money', 'Asian E-commerce'],
            'Region': ['Asia-Pacific', 'Europe', 'Latin America', 'Africa', 'Asia-Pacific'],
            'Deal Value ($M)': [150, 80, 120, 60, 200],
            'Expected Annual Volume ($B)': [2.5, 1.2, 1.8, 0.8, 3.2],
            'Status': ['Signed', 'Negotiation', 'Signed', 'Due Diligence', 'Signed'],
            'Go-Live': ['Q1 2025', 'Q2 2025', 'Q4 2024', 'Q3 2025', 'Q2 2025']
        }
        
        partnerships_df = st.data_editor(
            partnerships,
            column_config={
                "Deal Value ($M)": st.column_config.NumberColumn(
                    "Deal Value ($M)",
                    help="Total contract value",
                    format="$ %d"
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Current partnership status",
                    options=['Awareness', 'Interest', 'Evaluation', 'Negotiation', 'Signed', 'Live'],
                    required=True,
                ),
            },
            hide_index=True,
        )
        
        # Pipeline metrics
        st.subheader("Pipeline Health Metrics")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric("Total Pipeline Value", "$2.0B", "+15% QoQ")
        
        with metric_col2:
            st.metric("Conversion Rate", "16%", "+2% vs Target")
        
        with metric_col3:
            st.metric("Avg Deal Size", "$100M", "+5% YoY")
        
        with metric_col4:
            st.metric("Time to Close", "8.5 months", "-1.2 months YoY")
