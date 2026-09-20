# DATA PORTFOLIO - TEXAS DFPS COUNTY METRICS DASHBOARD

This dashboard visualizes county-level child population, removals, victims, and 
per-capita rates using the DFPS star-schema data warehouse built from Texas Open 
Data Portal datasets.

### Features
- Interactive county selector
- Population trends
- Removals per 1,000 children
- Victims per 1,000 children
- Fiscal-year aligned metrics
- Powered by MySQL + Dash + Plotly

### How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Update database credentials in config.py

3. Start the dashboard:
   python app.py
