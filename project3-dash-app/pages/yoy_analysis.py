"""

"""

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from config import DB_CONFIG

dash.register_page(__name__, path="/yoy")

def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT county_name, fiscal_year, removals,
               removals - LAG(removals) OVER (PARTITION BY county_name ORDER BY fiscal_year)
               AS yoy_change
        FROM vw_removals_agg
    """, conn)
    conn.close()
    return df

df = load_data()

layout = html.Div([
    html.H2("Year‑Over‑Year Removal Change"),

    dcc.Dropdown(
        id="county-yoy-dropdown",
        options=[{"label": c, "value": c} for c in sorted(df["county_name"].unique())],
        value="Travis",
        clearable=False
    ),

    dcc.Graph(id="yoy-chart")
])
