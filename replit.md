# Visa Cross-Border Analytics Dashboard

## Overview

This is a Streamlit-based analytics dashboard designed to showcase analytical capabilities for Visa's cross-border business unit. The application provides comprehensive tracking and analysis tools to help leadership monitor progress toward a 10% CAGR in cross-border revenues, with features spanning executive summary, performance tracking, opportunity identification, risk & compliance monitoring, and forecasting capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit (Python-based web application framework)
- **UI Components**: Multi-page application with tabbed navigation
- **Visualization**: Plotly for interactive charts and graphs
- **Styling**: Custom CSS with Visa brand colors (blue: #003087, green: #00A86B, red: #E31837)
- **Layout**: Wide layout with expandable sidebar for filters

### Backend Architecture
- **Language**: Python
- **Data Generation**: Mock data generator for demonstration purposes
- **Session Management**: Streamlit's built-in session state management
- **Modular Design**: Separate modules for pages, utilities, and chart generation

### Data Architecture
- **Data Storage**: In-memory data generation (no persistent database)
- **Data Generation**: Synthetic datasets created using numpy and pandas
- **Data Types**: Revenue data, KPI metrics, geographic data, product performance, opportunity analysis, risk metrics, and forecasting data

## Key Components

### 1. Main Application (`app.py`)
- Entry point and application configuration
- Global styling and branding implementation
- Session state initialization
- Navigation structure

### 2. Page Modules (`pages/`)
- **Executive Summary**: High-level KPI dashboard with gauges and scorecards
- **Performance Tracking**: Revenue trends, geographic breakdown, product performance, and KPI tables
- **Opportunity Identification**: Market opportunities, competitive analysis, and partnership pipeline
- **Risk & Compliance**: Risk dashboards, compliance monitoring, and incident analysis
- **Forecasting**: Scenario planning and revenue projections to 2030

### 3. Chart Generation (`charts.py`)
- Centralized chart creation with consistent Visa branding
- KPI gauges with traffic light color coding
- Interactive visualizations using Plotly
- Reusable chart components across all modules

### 4. Data Generator (`data_generator.py`)
- Mock data creation for demonstration purposes
- Generates realistic financial and operational metrics
- Supports multiple business segments and geographic regions
- Time-series data for trend analysis

### 5. Utility Modules (`utils/`)
- **Filters**: Global filtering system for time periods, segments, and geography
- **Export**: Data export functionality for CSV downloads and reporting

## Data Flow

1. **Initialization**: Data generator creates synthetic datasets on application startup
2. **User Interaction**: Global filters in sidebar modify data views across all pages
3. **Data Processing**: Filtered data is aggregated and processed for visualization
4. **Visualization**: Charts and metrics are rendered using Plotly with Visa branding
5. **Export**: Users can download processed data in CSV format

## External Dependencies

### Python Packages
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **numpy**: Numerical computing
- **datetime**: Date and time handling

### No External Data Sources
- All data is synthetically generated for demonstration
- No database connections or API integrations
- Self-contained application suitable for proof-of-concept demonstrations

## Deployment Strategy

### Development Environment
- Local development using Streamlit's built-in server
- Hot-reload capability for rapid development iteration
- No external infrastructure dependencies

### Production Considerations (Out of Scope)
- The current implementation is designed as a proof-of-concept
- Production deployment would require:
  - Integration with live Visa data sources
  - Database connectivity for persistent data storage
  - Enhanced security measures
  - Mobile responsiveness
  - Advanced AI/ML forecasting models
  - Scalable hosting infrastructure

### Key Architectural Decisions

1. **Streamlit Choice**: Selected for rapid prototyping and ease of deployment, allowing focus on analytics rather than web development complexity

2. **Mock Data Approach**: Synthetic data generation enables realistic demonstrations without requiring access to sensitive Visa data systems

3. **Modular Page Structure**: Separate page modules enable independent development of different dashboard sections and easier maintenance

4. **Plotly Integration**: Chosen for rich interactive visualizations that support the analytical requirements while maintaining Visa branding consistency

5. **Session State Management**: Leverages Streamlit's built-in session management to maintain filter states and user preferences across page navigation

6. **Brand-Consistent Styling**: Custom CSS implementation ensures visual alignment with Visa brand guidelines throughout the application