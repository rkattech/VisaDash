import streamlit as st
from datetime import datetime, timedelta

class GlobalFilters:
    def __init__(self):
        pass
    
    def render_filters(self):
        """Render global filter controls in sidebar"""
        filters = {}
        
        # Date range filter
        st.subheader("📅 Time Period")
        date_option = st.selectbox(
            "Select Period",
            ["Last 4 Quarters", "YTD", "Last 12 Months", "Custom Range"]
        )
        
        if date_option == "Custom Range":
            start_date = st.date_input("Start Date", datetime(2024, 1, 1))
            end_date = st.date_input("End Date", datetime.now())
            filters['date_range'] = (start_date, end_date)
        else:
            # Set predefined ranges
            end_date = datetime.now()
            start_date = end_date  # Default fallback
            
            if date_option == "Last 4 Quarters":
                start_date = end_date - timedelta(days=365)
            elif date_option == "YTD":
                start_date = datetime(end_date.year, 1, 1)
            elif date_option == "Last 12 Months":
                start_date = end_date - timedelta(days=365)
            
            filters['date_range'] = (start_date, end_date)
        
        # Segment filter
        st.subheader("🎯 Segments")
        available_segments = ["Travel", "E-commerce", "B2B", "Remittances"]
        selected_segments = st.multiselect(
            "Select Segments",
            available_segments,
            default=available_segments
        )
        filters['segments'] = selected_segments
        
        # Geographic filter
        st.subheader("🌍 Geography")
        available_regions = [
            "North America", "Europe", "Asia-Pacific", 
            "Latin America", "Middle East & Africa"
        ]
        selected_regions = st.multiselect(
            "Select Regions",
            available_regions,
            default=available_regions
        )
        filters['regions'] = selected_regions
        
        # Product filter
        st.subheader("💳 Products")
        available_products = ["Visa Direct", "B2B Connect", "Traditional Cards", "Other Services"]
        selected_products = st.multiselect(
            "Select Products",
            available_products,
            default=available_products
        )
        filters['products'] = selected_products
        
        # Currency filter
        st.subheader("💱 Currency")
        currency = st.selectbox(
            "Display Currency",
            ["USD", "EUR", "GBP", "JPY"],
            index=0
        )
        filters['currency'] = currency
        
        return filters
    
    def apply_filters(self, data, filters):
        """Apply filters to a dataset"""
        filtered_data = data.copy()
        
        # Apply date filter
        if 'date_range' in filters and 'date' in filtered_data.columns:
            start_date, end_date = filters['date_range']
            filtered_data = filtered_data[
                (filtered_data['date'] >= start_date) & 
                (filtered_data['date'] <= end_date)
            ]
        
        # Apply segment filter
        if 'segments' in filters and 'segment' in filtered_data.columns:
            if filters['segments']:
                filtered_data = filtered_data[
                    filtered_data['segment'].isin(filters['segments'])
                ]
        
        # Apply region filter  
        if 'regions' in filters and 'region' in filtered_data.columns:
            if filters['regions']:
                filtered_data = filtered_data[
                    filtered_data['region'].isin(filters['regions'])
                ]
        
        # Apply product filter
        if 'products' in filters and 'product' in filtered_data.columns:
            if filters['products']:
                filtered_data = filtered_data[
                    filtered_data['product'].isin(filters['products'])
                ]
        
        return filtered_data
    
    def get_filter_summary(self, filters):
        """Generate a summary of applied filters"""
        summary = []
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            summary.append(f"📅 {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        if 'segments' in filters and filters['segments']:
            if len(filters['segments']) < 4:
                summary.append(f"🎯 {', '.join(filters['segments'])}")
            else:
                summary.append("🎯 All segments")
        
        if 'regions' in filters and filters['regions']:
            if len(filters['regions']) < 5:
                summary.append(f"🌍 {', '.join(filters['regions'])}")
            else:
                summary.append("🌍 All regions")
        
        if 'products' in filters and filters['products']:
            if len(filters['products']) < 4:
                summary.append(f"💳 {', '.join(filters['products'])}")
            else:
                summary.append("💳 All products")
        
        return " | ".join(summary) if summary else "No filters applied"
