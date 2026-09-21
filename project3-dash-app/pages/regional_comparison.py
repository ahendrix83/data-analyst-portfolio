"""

"""

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from config import DB_CONFIG

dash.register_page(__name__, path="/regional")

def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT region_name, county_name, fiscal_year,
               removals_per_1000_children, victims_per_1000_children
        FROM vw_county_metrics
    """, conn)
    conn.close()
    return df

df = load_data()

layout = html.Div([
    html.H2("Regional Comparison"),

    dcc.Dropdown(
        id="region-dropdown",
        options=[{"label": r, "value": r} for r in sorted(df["region_name"].unique())],
        value="Region 7",
        clearable=False
    ),

    dcc.Graph(id="regional-removal-chart"),
    dcc.Graph(id="regional-victim-chart")
])
