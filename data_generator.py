import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataGenerator:
    def __init__(self):
        self.visa_blue = "#003087"
        self.visa_green = "#00A86B"
        self.visa_red = "#E31837"
        
        # Set random seed for reproducible demo data
        np.random.seed(42)
        random.seed(42)
        
        # Generate all mock datasets
        self.revenue_data = self._generate_revenue_data()
        self.kpi_data = self._generate_kpi_data()
        self.geographic_data = self._generate_geographic_data()
        self.product_data = self._generate_product_data()
        self.opportunity_data = self._generate_opportunity_data()
        self.risk_data = self._generate_risk_data()
        self.forecast_data = self._generate_forecast_data()
        
    def _generate_revenue_data(self):
        """Generate quarterly revenue and volume data from FY2024 to Q4 FY2025"""
        quarters = []
        base_date = datetime(2023, 10, 1)  # FY2024 Q1 start
        
        for i in range(8):  # 8 quarters of data
            quarter_start = base_date + timedelta(days=90*i)
            quarters.append({
                'quarter': f"FY{quarter_start.year + (1 if quarter_start.month >= 10 else 0)}-Q{((quarter_start.month - 1) // 3) % 4 + 1}",
                'date': quarter_start,
                'revenue_b': 2.8 + (i * 0.1) + np.random.normal(0, 0.05),  # Growing from $2.8B to $3.5B
                'volume_growth_pct': 8 + (i * 0.8) + np.random.normal(0, 1),  # Growing volume
                'segment': np.random.choice(['Travel', 'E-commerce', 'B2B', 'Remittances']),
                'region': np.random.choice(['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa'])
            })
        
        # Add segment and region breakdowns
        segments = ['Travel', 'E-commerce', 'B2B', 'Remittances']
        regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa']
        
        detailed_data = []
        for quarter_data in quarters:
            for segment in segments:
                for region in regions:
                    detailed_data.append({
                        'quarter': quarter_data['quarter'],
                        'date': quarter_data['date'],
                        'revenue_b': quarter_data['revenue_b'] * np.random.uniform(0.1, 0.3),
                        'volume_growth_pct': quarter_data['volume_growth_pct'] + np.random.normal(0, 2),
                        'segment': segment,
                        'region': region,
                        'transactions_m': np.random.uniform(50, 200),
                        'yield_pct': np.random.uniform(0.10, 0.15)
                    })
        
        return pd.DataFrame(detailed_data)
    
    def _generate_kpi_data(self):
        """Generate current KPI metrics"""
        return {
            'current_revenue': 3.5,  # $3.5B Q3 FY2025
            'achieved_cagr': 9.5,   # 9.5% CAGR
            'volume_growth': 13.0,  # 13% YoY
            'revenue_yield': 0.12,  # 0.12%
            'market_share': 22.0,   # 22%
            'target_revenue_2030': 22.5,  # $22.5B target
            'base_revenue_2024': 12.7,    # $12.7B FY2024
            'target_cagr': 10.0,          # 10% target CAGR
            'ytd_revenue': 13.5,          # $13.5B YTD
            'q3_volume_growth': 12.8      # 12.8% Q3 growth
        }
    
    def _generate_geographic_data(self):
        """Generate geographic performance data"""
        regions = [
            {'region': 'Asia-Pacific', 'revenue_share': 25, 'growth_rate': 18, 'penetration': 30},
            {'region': 'Europe', 'revenue_share': 22, 'growth_rate': 12, 'penetration': 45},
            {'region': 'North America', 'revenue_share': 20, 'growth_rate': 8, 'penetration': 55},
            {'region': 'Latin America', 'revenue_share': 18, 'growth_rate': 22, 'penetration': 25},
            {'region': 'Middle East & Africa', 'revenue_share': 15, 'growth_rate': 28, 'penetration': 15}
        ]
        
        # Add country-level data
        countries = []
        for region_data in regions:
            region = region_data['region']
            for i in range(5):  # 5 countries per region
                countries.append({
                    'country': f"Country_{region}_{i+1}",
                    'region': region,
                    'revenue_m': np.random.uniform(100, 1000),
                    'growth_rate': region_data['growth_rate'] + np.random.normal(0, 5),
                    'penetration': region_data['penetration'] + np.random.normal(0, 10),
                    'lat': np.random.uniform(-60, 60),
                    'lon': np.random.uniform(-180, 180)
                })
        
        return pd.DataFrame(countries)
    
    def _generate_product_data(self):
        """Generate product performance data"""
        products = [
            {
                'product': 'Visa Direct',
                'transactions_b': 2.5,
                'growth_rate': 20,
                'revenue_share': 35,
                'avg_transaction_value': 125
            },
            {
                'product': 'B2B Connect',
                'transactions_b': 0.8,
                'growth_rate': 25,
                'revenue_share': 30,
                'avg_transaction_value': 2500
            },
            {
                'product': 'Traditional Cards',
                'transactions_b': 4.2,
                'growth_rate': 8,
                'revenue_share': 25,
                'avg_transaction_value': 85
            },
            {
                'product': 'Other Services',
                'transactions_b': 1.1,
                'growth_rate': 15,
                'revenue_share': 10,
                'avg_transaction_value': 200
            }
        ]
        
        return pd.DataFrame(products)
    
    def _generate_opportunity_data(self):
        """Generate market opportunity data"""
        opportunities = []
        corridors = [
            'US-Mexico', 'UK-India', 'Saudi-Philippines', 'UAE-India', 'US-India',
            'Germany-Turkey', 'France-Algeria', 'Australia-China', 'Canada-India',
            'Singapore-Indonesia'
        ]
        
        for corridor in corridors:
            opportunities.append({
                'corridor': corridor,
                'potential_revenue_b': np.random.uniform(1, 10),
                'current_penetration': np.random.uniform(5, 40),
                'market_size_b': np.random.uniform(10, 100),
                'visa_share': np.random.uniform(10, 35),
                'growth_potential': np.random.uniform(15, 50)
            })
        
        return pd.DataFrame(opportunities)
    
    def _generate_risk_data(self):
        """Generate risk and compliance metrics"""
        return {
            'fraud_rate': 0.45,      # <0.5% target
            'chargeback_ratio': 0.8,  # 1% target
            'compliance_score': 95,   # 95% score
            'transaction_cost': 0.8,  # <1% FSB target
            'aml_alerts': 23,
            'regulatory_incidents': 2,
            'data_breaches': 0,
            'uptime_pct': 99.98
        }
    
    def _generate_forecast_data(self):
        """Generate forecasting scenarios"""
        base_year = 2024
        years = list(range(base_year, 2031))
        
        scenarios = {
            'conservative': {'cagr': 8, 'volatility': 0.02},
            'base_case': {'cagr': 10, 'volatility': 0.03},
            'optimistic': {'cagr': 12, 'volatility': 0.04}
        }
        
        forecast_data = []
        base_revenue = 12.7  # FY2024 base
        
        for scenario_name, params in scenarios.items():
            for i, year in enumerate(years):
                if year == base_year:
                    revenue = base_revenue
                else:
                    years_elapsed = year - base_year
                    growth_factor = (1 + params['cagr']/100) ** years_elapsed
                    noise = np.random.normal(0, params['volatility'])
                    revenue = base_revenue * growth_factor * (1 + noise)
                
                forecast_data.append({
                    'year': year,
                    'scenario': scenario_name,
                    'revenue_b': revenue,
                    'confidence_lower': revenue * 0.9,
                    'confidence_upper': revenue * 1.1
                })
        
        return pd.DataFrame(forecast_data)
    
    def get_filtered_data(self, data, filters):
        """Apply global filters to any dataset"""
        filtered_data = data.copy()
        
        if 'date_range' in filters and filters['date_range']:
            if 'date' in filtered_data.columns:
                start_date, end_date = filters['date_range']
                filtered_data = filtered_data[
                    (filtered_data['date'] >= start_date) & 
                    (filtered_data['date'] <= end_date)
                ]
        
        if 'segments' in filters and filters['segments']:
            if 'segment' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['segment'].isin(filters['segments'])]
        
        if 'regions' in filters and filters['regions']:
            if 'region' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['region'].isin(filters['regions'])]
        
        return filtered_data
