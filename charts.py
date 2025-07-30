import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ChartGenerator:
    def __init__(self):
        self.visa_blue = "#003087"
        self.visa_green = "#00A86B"
        self.visa_red = "#E31837"
        self.visa_colors = [self.visa_blue, self.visa_green, "#FFB800", "#9013FE", "#FF6B35"]
    
    def create_kpi_gauge(self, value, target, title, suffix="", color_thresholds=None):
        """Create a KPI gauge chart with traffic light colors"""
        if color_thresholds is None:
            color_thresholds = {'green': 90, 'yellow': 70}
        
        # Determine color based on performance vs target
        if value >= target * (color_thresholds['green'] / 100):
            color = self.visa_green
        elif value >= target * (color_thresholds['yellow'] / 100):
            color = "#FFB800"
        else:
            color = self.visa_red
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 16}},
            delta = {'reference': target, 'suffix': suffix},
            gauge = {
                'axis': {'range': [None, target * 1.2]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, target * 0.7], 'color': "lightgray"},
                    {'range': [target * 0.7, target * 0.9], 'color': "yellow"},
                    {'range': [target * 0.9, target * 1.2], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': target
                }
            }
        ))
        
        fig.update_layout(height=300, margin=dict(t=50, b=50, l=50, r=50))
        return fig
    
    def create_revenue_trend(self, data):
        """Create revenue trend line chart with actual vs target"""
        fig = go.Figure()
        
        # Group by quarter and sum revenue
        quarterly_data = data.groupby('quarter')['revenue_b'].sum().reset_index()
        quarterly_data = quarterly_data.sort_values('quarter')
        
        # Actual revenue line
        fig.add_trace(go.Scatter(
            x=quarterly_data['quarter'],
            y=quarterly_data['revenue_b'],
            mode='lines+markers',
            name='Actual Revenue',
            line=dict(color=self.visa_blue, width=3),
            marker=dict(size=8)
        ))
        
        # Target line (10% CAGR trajectory)
        base_revenue = 12.7  # FY2024 base
        target_revenues = []
        for i, quarter in enumerate(quarterly_data['quarter']):
            # Approximate quarterly growth for 10% annual CAGR
            quarterly_growth = 0.024  # ~10% annual / 4 quarters
            target_revenue = base_revenue * (1 + quarterly_growth) ** i
            target_revenues.append(target_revenue)
        
        fig.add_trace(go.Scatter(
            x=quarterly_data['quarter'],
            y=target_revenues,
            mode='lines+markers',
            name='Target (10% CAGR)',
            line=dict(color=self.visa_green, width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Cross-Border Revenue Trajectory to 2030 Target",
            xaxis_title="Quarter",
            yaxis_title="Revenue ($ Billions)",
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_geographic_heatmap(self, geographic_data):
        """Create geographic performance heatmap"""
        fig = px.scatter_geo(
            geographic_data,
            lat='lat',
            lon='lon',
            size='revenue_m',
            color='growth_rate',
            hover_name='country',
            hover_data={'region': True, 'penetration': True, 'revenue_m': ':,.0f'},
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Global Cross-Border Performance Heatmap"
        )
        
        fig.update_layout(
            height=500,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        return fig
    
    def create_product_donut(self, product_data):
        """Create product revenue share donut chart"""
        fig = go.Figure(data=[go.Pie(
            labels=product_data['product'],
            values=product_data['revenue_share'],
            hole=.3,
            marker_colors=self.visa_colors
        )])
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Revenue Share: %{value}%<br>Transactions: %{customdata:.1f}B<extra></extra>',
            customdata=product_data['transactions_b']
        )
        
        fig.update_layout(
            title="Product Revenue Share",
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )
        
        return fig
    
    def create_opportunity_bubble(self, opportunity_data):
        """Create market opportunity bubble chart"""
        fig = px.scatter(
            opportunity_data,
            x='potential_revenue_b',
            y='current_penetration',
            size='market_size_b',
            color='visa_share',
            hover_name='corridor',
            hover_data={'growth_potential': ':,.1f%'},
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Market Opportunity Analysis",
            labels={
                'potential_revenue_b': 'Potential Revenue ($B)',
                'current_penetration': 'Current Penetration (%)',
                'visa_share': 'Visa Market Share (%)'
            }
        )
        
        fig.update_layout(height=500)
        return fig
    
    def create_risk_dashboard(self, risk_data):
        """Create risk metrics dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Fraud Rate', 'Compliance Score', 'Chargeback Ratio', 'Transaction Cost'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Fraud Rate Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=risk_data['fraud_rate'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Fraud Rate (%)"},
            gauge={
                'axis': {'range': [None, 1.0]},
                'bar': {'color': self.visa_green if risk_data['fraud_rate'] < 0.5 else self.visa_red},
                'steps': [{'range': [0, 0.5], 'color': 'lightgreen'},
                         {'range': [0.5, 1.0], 'color': 'lightcoral'}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.5}
            }
        ), row=1, col=1)
        
        # Compliance Score Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=risk_data['compliance_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Compliance Score (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': self.visa_green if risk_data['compliance_score'] >= 90 else self.visa_red},
                'steps': [{'range': [0, 70], 'color': 'lightcoral'},
                         {'range': [70, 90], 'color': 'yellow'},
                         {'range': [90, 100], 'color': 'lightgreen'}],
                'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ), row=1, col=2)
        
        # Chargeback Ratio Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=risk_data['chargeback_ratio'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Chargeback Ratio (%)"},
            gauge={
                'axis': {'range': [0, 2.0]},
                'bar': {'color': self.visa_green if risk_data['chargeback_ratio'] < 1.0 else self.visa_red},
                'steps': [{'range': [0, 1.0], 'color': 'lightgreen'},
                         {'range': [1.0, 2.0], 'color': 'lightcoral'}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1.0}
            }
        ), row=2, col=1)
        
        # Transaction Cost Gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=risk_data['transaction_cost'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Transaction Cost (%)"},
            gauge={
                'axis': {'range': [0, 2.0]},
                'bar': {'color': self.visa_green if risk_data['transaction_cost'] < 1.0 else self.visa_red},
                'steps': [{'range': [0, 1.0], 'color': 'lightgreen'},
                         {'range': [1.0, 2.0], 'color': 'lightcoral'}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1.0}
            }
        ), row=2, col=2)
        
        fig.update_layout(height=600, title_text="Risk & Compliance Dashboard")
        return fig
    
    def create_forecast_scenarios(self, forecast_data):
        """Create forecasting scenarios with confidence bands"""
        fig = go.Figure()
        
        scenarios = ['conservative', 'base_case', 'optimistic']
        colors = [self.visa_red, self.visa_blue, self.visa_green]
        
        for i, scenario in enumerate(scenarios):
            scenario_data = forecast_data[forecast_data['scenario'] == scenario]
            
            # Main forecast line
            fig.add_trace(go.Scatter(
                x=scenario_data['year'],
                y=scenario_data['revenue_b'],
                mode='lines+markers',
                name=f'{scenario.replace("_", " ").title()}',
                line=dict(color=colors[i], width=3),
                marker=dict(size=6)
            ))
            
            # Confidence bands for base case only
            if scenario == 'base_case':
                fig.add_trace(go.Scatter(
                    x=list(scenario_data['year']) + list(scenario_data['year'][::-1]),
                    y=list(scenario_data['confidence_upper']) + list(scenario_data['confidence_lower'][::-1]),
                    fill='toself',
                    fillcolor='rgba(0,48,135,0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=False,
                    name='Confidence Interval'
                ))
        
        # Add target line at $22.5B for 2030
        fig.add_hline(y=22.5, line_dash="dash", line_color="green",
                      annotation_text="2030 Target ($22.5B)")
        
        fig.update_layout(
            title="Revenue Forecasting Scenarios to 2030",
            xaxis_title="Year",
            yaxis_title="Revenue ($ Billions)",
            height=500,
            hovermode='x unified'
        )
        
        return fig
