import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from charts import ChartGenerator

def render(data_generator, filters):
    st.title("🔮 Forecasting & Scenario Planning")
    
    chart_gen = ChartGenerator()
    
    # Scenario parameters
    st.subheader("Scenario Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Economic Factors**")
        gdp_growth = st.slider("Global GDP Growth (%)", 1.0, 5.0, 2.8, 0.1)
        inflation_rate = st.slider("Average Inflation (%)", 1.0, 8.0, 3.2, 0.1)
        
    with col2:
        st.write("**Market Factors**")
        digitization_rate = st.slider("Payment Digitization (%/year)", 5.0, 20.0, 12.0, 0.5)
        competition_intensity = st.slider("Competition Intensity", 1, 10, 6)
        
    with col3:
        st.write("**Visa Specific**")
        investment_level = st.slider("R&D Investment ($B)", 0.5, 3.0, 1.5, 0.1)
        partnership_success = st.slider("Partnership Success Rate (%)", 10, 50, 25, 1)
    
    # Update forecast based on parameters
    if st.button("🔄 Update Forecast"):
        st.session_state.forecast_updated = True
    
    # Base forecast scenarios
    st.subheader("Revenue Forecast Scenarios to 2030")
    
    forecast_chart = chart_gen.create_forecast_scenarios(data_generator.forecast_data)
    st.plotly_chart(forecast_chart, use_container_width=True)
    
    # Scenario comparison table
    st.subheader("Scenario Comparison")
    
    scenario_data = {
        'Scenario': ['Conservative (8% CAGR)', 'Base Case (10% CAGR)', 'Optimistic (12% CAGR)'],
        '2025 Revenue ($B)': [14.2, 14.8, 15.4],
        '2027 Revenue ($B)': [16.8, 18.5, 20.4],
        '2030 Revenue ($B)': [18.9, 22.5, 26.8],
        'Probability': ['30%', '50%', '20%'],
        'Key Drivers': [
            'Economic slowdown, increased competition',
            'Steady growth, successful partnerships',
            'Accelerated digitization, market expansion'
        ]
    }
    
    st.dataframe(scenario_data, use_container_width=True, hide_index=True)
    
    # Monte Carlo simulation results
    st.subheader("Monte Carlo Simulation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate Monte Carlo data
        np.random.seed(42)
        n_simulations = 1000
        final_revenues = []
        
        for _ in range(n_simulations):
            # Random factors affecting growth
            economic_factor = np.random.normal(1.0, 0.15)
            market_factor = np.random.normal(1.0, 0.12)
            execution_factor = np.random.normal(1.0, 0.10)
            
            # Base case adjusted by factors
            adjusted_cagr = 10 * economic_factor * market_factor * execution_factor
            final_revenue = 12.7 * (1 + adjusted_cagr/100) ** 6
            final_revenues.append(final_revenue)
        
        # Distribution chart
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=final_revenues, nbinsx=50, name='Simulated Outcomes'))
        fig.add_vline(x=22.5, line_dash="dash", line_color="green", 
                     annotation_text="Target ($22.5B)")
        fig.add_vline(x=np.mean(final_revenues), line_dash="dash", line_color="blue",
                     annotation_text=f"Mean (${np.mean(final_revenues):.1f}B)")
        
        fig.update_layout(
            title="2030 Revenue Distribution (1,000 simulations)",
            xaxis_title="Revenue ($B)",
            yaxis_title="Frequency",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monte Carlo statistics
        percentiles = np.percentile(final_revenues, [10, 25, 50, 75, 90])
        prob_target = (np.array(final_revenues) >= 22.5).mean() * 100
        
        st.info(f"""
        **Monte Carlo Results:**
        
        **Probability of reaching $22.5B target: {prob_target:.1f}%**
        
        **Revenue Percentiles:**
        - 10th percentile: ${percentiles[0]:.1f}B
        - 25th percentile: ${percentiles[1]:.1f}B
        - 50th percentile: ${percentiles[2]:.1f}B
        - 75th percentile: ${percentiles[3]:.1f}B  
        - 90th percentile: ${percentiles[4]:.1f}B
        
        **Mean: ${np.mean(final_revenues):.1f}B**
        **Std Dev: ${np.std(final_revenues):.1f}B**
        """)
    
    # Sensitivity analysis
    st.subheader("Sensitivity Analysis")
    
    # Create sensitivity data
    variables = ['Travel Recovery', 'E-commerce Growth', 'B2B Adoption', 'New Markets', 'Competition', 'Regulations']
    base_impact = [0, 0, 0, 0, 0, 0]  # Base case
    optimistic_impact = [+15, +20, +25, +30, -5, +5]  # Optimistic scenario
    pessimistic_impact = [-10, -8, -12, -15, -15, -10]  # Pessimistic scenario
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Pessimistic',
        x=variables,
        y=pessimistic_impact,
        marker_color='red'
    ))
    
    fig.add_trace(go.Bar(
        name='Base Case',
        x=variables,
        y=base_impact,
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        name='Optimistic',
        x=variables,
        y=optimistic_impact,
        marker_color='green'
    ))
    
    fig.update_layout(
        title="Revenue Impact by Variable (% change vs base case)",
        xaxis_title="Variables",
        yaxis_title="Revenue Impact (%)",
        barmode='group',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Dynamic scenario builder
    st.subheader("Custom Scenario Builder")
    
    st.write("**Adjust key variables to see impact on 2030 revenue forecast:**")
    
    scenario_col1, scenario_col2 = st.columns(2)
    
    with scenario_col1:
        travel_recovery = st.slider("Travel Recovery vs 2019 (%)", 80, 120, 100)
        ecommerce_growth = st.slider("E-commerce Annual Growth (%)", 5, 25, 15)
        b2b_penetration = st.slider("B2B Digital Penetration (%)", 20, 80, 50)
        
    with scenario_col2:
        new_market_entry = st.slider("New Market Revenue Contribution (%)", 0, 20, 8)
        competitive_pressure = st.slider("Competitive Pressure Impact (%)", -20, 0, -8)
        regulatory_support = st.slider("Regulatory Environment Impact (%)", -10, 10, 2)
    
    # Calculate custom scenario impact
    custom_impact = (
        (travel_recovery - 100) * 0.3 +
        (ecommerce_growth - 15) * 0.2 +
        (b2b_penetration - 50) * 0.15 +
        new_market_entry * 0.1 +
        competitive_pressure * 0.15 +
        regulatory_support * 0.1
    )
    
    base_2030_revenue = 22.5
    custom_2030_revenue = base_2030_revenue * (1 + custom_impact / 100)
    required_cagr = ((custom_2030_revenue / 12.7) ** (1/6) - 1) * 100
    
    # Custom scenario results
    st.subheader("Custom Scenario Results")
    
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.metric("2030 Revenue Forecast", f"${custom_2030_revenue:.1f}B", 
                 f"{custom_2030_revenue - base_2030_revenue:+.1f}B vs Base")
    
    with result_col2:
        st.metric("Required CAGR", f"{required_cagr:.1f}%", 
                 f"{required_cagr - 10:+.1f}% vs Target")
    
    with result_col3:
        if custom_2030_revenue >= 22.5:
            st.success(f"✅ Target Achieved")
        else:
            st.error(f"❌ ${22.5 - custom_2030_revenue:.1f}B shortfall")
    
    # Action recommendations
    st.subheader("Strategic Recommendations")
    
    if custom_2030_revenue < 22.0:
        st.error("""
        🚨 **Immediate Action Required**
        - Accelerate partnership acquisitions
        - Increase investment in high-growth segments
        - Consider strategic acquisitions
        - Enhance competitive positioning
        """)
    elif custom_2030_revenue < 22.5:
        st.warning("""
        ⚠️ **Monitor and Adjust**
        - Track key performance indicators closely
        - Prepare contingency plans
        - Optimize operational efficiency
        - Focus on retention strategies
        """)
    else:
        st.success("""
        ✅ **On Track for Success**
        - Continue current strategic initiatives
        - Explore additional growth opportunities
        - Maintain competitive advantages
        - Consider raising targets
        """)
