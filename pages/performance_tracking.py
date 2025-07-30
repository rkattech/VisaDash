import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from charts import ChartGenerator

def render(data_generator, filters):
    st.title("📈 Performance Tracking")
    
    chart_gen = ChartGenerator()
    
    # Tabs for different performance views
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue & Volume Trends", "Geographic Breakdown", "Product Performance", "KPI Table"])
    
    with tab1:
        st.subheader("Revenue and Volume Trends")
        
        # Time period selector
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            view_mode = st.selectbox("View Mode", ["Quarterly", "YTD", "Trailing 12M"])
        with time_col2:
            segment_filter = st.multiselect("Segments", 
                                          ["Travel", "E-commerce", "B2B", "Remittances"],
                                          default=["Travel", "E-commerce", "B2B", "Remittances"])
        
        # Filter data
        filtered_data = data_generator.get_filtered_data(data_generator.revenue_data, filters)
        if segment_filter:
            filtered_data = filtered_data[filtered_data['segment'].isin(segment_filter)]
        
        # Dual-axis chart for revenue and volume
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Revenue bars
        quarterly_revenue = filtered_data.groupby(['quarter', 'segment'])['revenue_b'].sum().unstack().fillna(0)
        for segment in quarterly_revenue.columns:
            fig.add_trace(
                go.Bar(x=quarterly_revenue.index, y=quarterly_revenue[segment], 
                      name=f"{segment} Revenue", showlegend=True),
                secondary_y=False,
            )
        
        # Volume growth line
        quarterly_volume = filtered_data.groupby('quarter')['volume_growth_pct'].mean()
        fig.add_trace(
            go.Scatter(x=quarterly_volume.index, y=quarterly_volume.values,
                      mode='lines+markers', name='Volume Growth %',
                      line=dict(color='red', width=3)),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Quarter")
        fig.update_yaxes(title_text="Revenue ($ Billions)", secondary_y=False)
        fig.update_yaxes(title_text="Volume Growth (%)", secondary_y=True)
        fig.update_layout(height=500, title="Revenue and Volume Performance")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment performance summary
        segment_summary = filtered_data.groupby('segment').agg({
            'revenue_b': 'sum',
            'volume_growth_pct': 'mean',
            'transactions_m': 'sum'
        }).round(2)
        
        st.subheader("Segment Performance Summary")
        st.dataframe(segment_summary, use_container_width=True)
    
    with tab2:
        st.subheader("Geographic Breakdown")
        
        # Geographic performance heatmap
        geo_heatmap = chart_gen.create_geographic_heatmap(data_generator.geographic_data)
        st.plotly_chart(geo_heatmap, use_container_width=True)
        
        # Regional performance bars
        col1, col2 = st.columns(2)
        
        with col1:
            regional_data = data_generator.geographic_data.groupby('region').agg({
                'revenue_m': 'sum',
                'growth_rate': 'mean',
                'penetration': 'mean'
            }).round(1)
            
            fig = px.bar(regional_data.reset_index(), 
                        x='region', y='revenue_m',
                        title="Revenue by Region ($M)",
                        color='growth_rate',
                        color_continuous_scale=['red', 'yellow', 'green'])
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(regional_data.reset_index(), 
                        x='region', y='penetration',
                        title="Market Penetration by Region (%)",
                        color='penetration',
                        color_continuous_scale=['red', 'yellow', 'green'])
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top corridors table
        st.subheader("Top 10 Growth Corridors")
        top_corridors = data_generator.geographic_data.nlargest(10, 'growth_rate')[
            ['country', 'region', 'revenue_m', 'growth_rate', 'penetration']
        ]
        st.dataframe(top_corridors, use_container_width=True)
    
    with tab3:
        st.subheader("Product and Segment Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Product revenue share donut
            product_donut = chart_gen.create_product_donut(data_generator.product_data)
            st.plotly_chart(product_donut, use_container_width=True)
        
        with col2:
            # Product growth rates
            fig = px.bar(data_generator.product_data, 
                        x='product', y='growth_rate',
                        title="Product Growth Rates (%)",
                        color='growth_rate',
                        color_continuous_scale=['red', 'yellow', 'green'])
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Product metrics table
        st.subheader("Detailed Product Metrics")
        product_metrics = data_generator.product_data.copy()
        product_metrics['Revenue ($B)'] = product_metrics['revenue_share'] * 0.035  # Approximate revenue
        product_metrics_display = product_metrics[['product', 'Revenue ($B)', 'transactions_b', 'growth_rate', 'avg_transaction_value']]
        product_metrics_display.columns = ['Product', 'Revenue ($B)', 'Transactions (B)', 'Growth Rate (%)', 'Avg Transaction ($)']
        st.dataframe(product_metrics_display, use_container_width=True)
    
    with tab4:
        st.subheader("KPI Performance Table")
        
        # Create comprehensive KPI table
        kpi_table_data = {
            'KPI': [
                'Volume Growth Rate', 'Revenue Growth Rate', 'Market Share', 
                'Revenue Yield', 'Customer Acquisition', 'Transaction Success Rate',
                'Cross-Border Penetration', 'Average Transaction Value'
            ],
            'Target': ['15%', '12%', '25%', '0.15%', '10K/month', '99.5%', '35%', '$150'],
            'Current': ['13%', '9.5%', '22%', '0.12%', '8.5K/month', '99.7%', '30%', '$125'],
            'YoY Change': ['+2.1%', '+1.8%', '+2.1%', '+0.01%', '+15%', '+0.1%', '+5%', '+8%'],
            'Status': ['⚠️ Below', '⚠️ Below', '⚠️ Below', '⚠️ Below', '⚠️ Below', '✅ Above', '⚠️ Below', '⚠️ Below'],
            'Source': ['Internal', 'Internal', 'Industry', 'Internal', 'CRM', 'Internal', 'Survey', 'Internal']
        }
        
        kpi_df = st.data_editor(
            kpi_table_data,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Performance vs target",
                ),
            },
            disabled=["KPI", "Source"],
            hide_index=True,
        )
        
        # Performance summary
        total_kpis = len(kpi_df)
        above_target = len([status for status in kpi_df['Status'] if '✅' in status])
        performance_pct = (above_target / total_kpis) * 100
        
        if performance_pct >= 70:
            st.success(f"✅ Overall Performance: {performance_pct:.1f}% of KPIs above target")
        elif performance_pct >= 50:
            st.warning(f"⚠️ Overall Performance: {performance_pct:.1f}% of KPIs above target")
        else:
            st.error(f"🚨 Overall Performance: {performance_pct:.1f}% of KPIs above target - Action Required")
