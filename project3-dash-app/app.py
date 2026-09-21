"""
Dash App in production

"""



import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1("DFPS Multi‑Page Dashboard", style={"textAlign": "center"}),

    dbc.Nav(
        [
            dbc.NavLink("County Metrics", href="/", active="exact"),
            dbc.NavLink("Statewide Trends", href="/statewide", active="exact"),
            dbc.NavLink("Regional Comparison", href="/regional", active="exact"),
            dbc.NavLink("YOY Analysis", href="/yoy", active="exact"),
            dbc.NavLink("Data Quality", href="/quality", active="exact"),
            dbc.NavLink("Data Quality", href="/region-trend", active="exact"),

        ],
        pills=True,
        justified=True,
        style={"marginBottom": "20px"}
    ),

    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=True)
