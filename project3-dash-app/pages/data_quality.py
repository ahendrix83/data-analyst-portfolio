"""

"""

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from config import DB_CONFIG

dash.register_page(__name__, path="/quality")

def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT county_name, fiscal_year, removals, victims, child_pop
        FROM vw_county_metrics
    """, conn)
    conn.close()
    return df

df = load_data()

missing_pop = df[df["child_pop"].isna()]
zero_removals = df[df["removals"] == 0]

layout = html.Div([
    html.H2("Data Quality Checks"),

    html.H3("Counties with Missing Population Data"),
    dcc.Graph(
        figure=px.bar(missing_pop, x="county_name", y="fiscal_year")
    ),

    html.H3("Counties with Zero Removals"),
    dcc.Graph(
        figure=px.bar(zero_removals, x="county_name", y="fiscal_year")
    )
])
