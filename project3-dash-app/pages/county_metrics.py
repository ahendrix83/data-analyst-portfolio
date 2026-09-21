"""

"""

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from config import DB_CONFIG

dash.register_page(__name__, path="/")

def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT county_name, 
                fiscal_year, 
                child_pop, 
                removals, 
                victims,
                removals_per_1000_children, 
                victims_per_1000_children
        FROM vw_county_metrics
    """, conn)
    conn.close()
    return df

df = load_data()

layout = html.Div([
    html.H2("County Metrics Explorer"),

    dcc.Dropdown(
        id="county-dropdown",
        options=[{"label": c, "value": c} for c in sorted(df["county_name"].unique())],
        value="Travis",
        clearable=False
    ),

    dcc.Graph(id="pop-chart"),
    dcc.Graph(id="removal-chart"),
    dcc.Graph(id="victim-chart")
])
