import streamlit as st
import pandas as pd
from io import BytesIO
import base64

class ExportUtils:
    @staticmethod
    def export_to_csv(data, filename="visa_dashboard_data.csv"):
        """Export data to CSV format"""
        if isinstance(data, dict):
            # Convert dict to DataFrame
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            st.error("Data format not supported for CSV export")
            return None
        
        # Convert DataFrame to CSV
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        return csv_buffer.getvalue()
    
    @staticmethod
    def create_download_link(data, filename, file_format="csv"):
        """Create a download link for the data"""
        if file_format.lower() == "csv":
            csv_data = ExportUtils.export_to_csv(data, filename)
            if csv_data:
                b64 = base64.b64encode(csv_data).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
                return href
        
        return None
    
    @staticmethod
    def export_chart_data(chart_data, chart_title="chart_data"):
        """Export chart data for external use"""
        filename = f"{chart_title.lower().replace(' ', '_')}_data.csv"
        return ExportUtils.export_to_csv(chart_data, filename)
    
    @staticmethod
    def generate_summary_report(data_generator):
        """Generate a comprehensive summary report"""
        kpi_data = data_generator.kpi_data
        
        summary = {
            'Metric': [
                'Current Revenue (Q3 FY2025)',
                'Achieved CAGR',
                'Volume Growth',
                'Market Share',
                'Revenue Yield',
                'Target Revenue 2030',
                'YTD Revenue'
            ],
            'Value': [
                f"${kpi_data['current_revenue']:.1f}B",
                f"{kpi_data['achieved_cagr']:.1f}%",
                f"{kpi_data['volume_growth']:.1f}%",
                f"{kpi_data['market_share']:.1f}%",
                f"{kpi_data['revenue_yield']:.2f}%",
                f"${kpi_data['target_revenue_2030']:.1f}B",
                f"${kpi_data['ytd_revenue']:.1f}B"
            ],
            'Status': [
                '✅ On Track',
                '⚠️ Below Target',
                '✅ Above Target',
                '⚠️ Below Target',
                '⚠️ Below Target',
                '📈 Target',
                '✅ On Track'
            ]
        }
        
        return pd.DataFrame(summary)
