"""

"""

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from config import DB_CONFIG

dash.register_page(__name__, path="/statewide")

def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT fiscal_year,
               SUM(removals) AS statewide_removals,
               SUM(victims) AS statewide_victims
        FROM vw_county_metrics
        GROUP BY fiscal_year
        ORDER BY fiscal_year
    """, conn)
    conn.close()
    return df

df = load_data()

layout = html.Div([
    html.H2("Statewide Trends"),

    dcc.Graph(
        figure=px.line(df, x="fiscal_year", y="statewide_removals",
                       title="Statewide Removals Over Time")
    ),

    dcc.Graph(
        figure=px.line(df, x="fiscal_year", y="statewide_victims",
                       title="Statewide Confirmed Victims Over Time")
    )
])
