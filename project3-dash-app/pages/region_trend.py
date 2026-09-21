# Program region_trend.py
# Description: 
# 	<what the program does> 
# Author: Ashley Hendrix
# Date: Sept. 20, 2026
# Revised: 
# 	<revision date> 
# 	<revision date> 

# list libraries used
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import mysql.connector
from config import DB_CONFIG

# Declare global constants 
dash.register_page(__name__, path="/region-trend", name="Region Trend")


# Load Region-Level Data
def load_region_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(
        """
        SELECT
            cd.region_name,
            cm.fiscal_year,
            SUM(cm.removals) AS total_removals
        FROM vw_county_metrics cm
        JOIN county_dim cd ON cm.county_code = cd.county_code
        WHERE cm.fiscal_year BETWEEN 2016 AND 2025
        GROUP BY cd.region_name, cm.fiscal_year
        ORDER BY cd.region_name, cm.fiscal_year;
        """,
        conn
    )
    conn.close()
    return df

df = load_region_data()


# Calculate Slopes (Trend Strength)
def calculate_slopes(df):
    slopes = []
    for region in df["region_name"].unique():
        dff = df[df["region_name"] == region]

        # X = fiscal years, Y = removals
        x = dff["fiscal_year"]
        y = dff["total_removals"]

        # Fit a line: slope tells direction & strength
        slope = np.polyfit(x, y, 1)[0]

        slopes.append({
            "region_name": region,
            "slope": slope
        })

    return pd.DataFrame(slopes)

slopes_df = calculate_slopes(df)

# Identify strongest downward trend (most negative slope)
strongest_decline = slopes_df.sort_values("slope").iloc[0]


# Page Layout
layout = html.Div([
    html.H2("Regional Removal Trends (2016–2025)"),

    html.P(
        "This page analyzes DFPS regions to determine which one shows the strongest "
        "downward trend in removals over time."
    ),

    # Display strongest declining region
    html.Div(
        [
            html.H3(f"Region with Strongest Downward Trend: {strongest_decline['region_name']}"),
            html.P(f"Slope: {round(strongest_decline['slope'], 2)} "
                   "(More negative = stronger downward trend)")
        ],
        style={
            "background": "white",
            "padding": "15px",
            "borderRadius": "10px",
            "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)",
            "marginBottom": "20px"
        }
    ),

    # Trend Line Chart
    dcc.Graph(
        id="region-trend-chart",
        figure=px.line(
            df,
            x="fiscal_year",
            y="total_removals",
            color="region_name",
            markers=True,
            title="Removals Over Time by Region (2016–2025)",
            labels={
                "fiscal_year": "Fiscal Year",
                "total_removals": "Total Removals",
                "region_name": "Region"
            }
        ).update_layout(template="plotly_white")
    ),

    # Slope Ranking Chart
    html.H3("Trend Strength by Region (Slope Values)"),
    dcc.Graph(
        id="slope-chart",
        figure=px.bar(
            slopes_df.sort_values("slope"),
            x="region_name",
            y="slope",
            title="Slope of Removal Trend by Region",
            labels={
                "region_name": "Region",
                "slope": "Trend Slope (Negative = Decline)"
            }
        ).update_layout(template="plotly_white")
    )
])
