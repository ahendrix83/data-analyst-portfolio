#------------------------------------------------------------------
'''
connects to MYSQL database and retrieves data for the dashboard
quries the database and returns the results as a pandas dataframe
builds interactive visualizations using plotly and dash
lets users filter and explore the data through the dashboard'''

#------------------------------------------------------------------

# Libraries and dependencies
import pandas as pd
import mysql.connector
import dash
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from config import DB_CONFIG

# Load  data from the MySQL database
def load_dfps_data():
    conn = mysql.connector.connect(**DB_CONFIG)

    query = """
    SELECT
        county_name,
        fiscal_year,
        child_pop,
        removals,
        victims,
        removals_per_1000_children,
        victims_per_1000_children
    FROM vw_county_metrics
    ORDER BY county_name, fiscal_year;"""

    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_dfps_data()

# DASH APP

app = dash.Dash(__name__)

app.layout = html.Div(className='dashboard-container', children=[
    html.H1('Data Portfolio: DFPS County Metrics Dashboard'),

    html.Div(className='dropdown-containers', children=[
        html.Label('Select Texas County'),
        dcc.Dropdown(
            id="county-dropdown",
            # Fix 1: Changed "Label" to lowercase "label"
            options=[{"label": c, "value": c} for c in sorted(df['county_name'].unique())],
            value='Travis',
            clearable=False
        ), # default is travis county , musts be filled
    ]), 
    html.Div(className='chart-card', children=[
        # Fix 2: Changed the closing square bracket ] to a closing parenthesis )
        dcc.Graph(id='population-chart')    
    ]),

    html.Div(className='chart-card', children=[
        dcc.Graph(id='removal-rate-chart')
    ]),

    html.Div(className='chart-card', children=[
        dcc.Graph(id='victim-rate-chart')
    ]),

    html.Div(
    "DFPS Data Visualization — Built with Dash & MySQL deveopled by Ashley Hendrix",
    style={"textAlign": "center", "color": "#535b5c", "marginTop": "40px"})

])# end app layout

# CALLBACKS
@app.callback(
    [
        Output("population-chart", "figure"),
        Output("removal-rate-chart", "figure"),
        Output("victim-rate-chart","figure")
    ], # end output
    [Input('county-dropdown', 'value')]
) # end app call back

def update_charts(county):
    dff = df[df['county_name'] == county]

    fig_pop = px.line(
        dff,
        x='fiscal_year',
        y='child_pop',
        title=f"Texas Child Population Over Time for {county} County",
        labels={
            "fiscal_year": "DFPS Fiscal Year",
            "child_pop":"Texas Child Populations (Ages 0 - 17)"
        }
    )
    fig_pop.update_layout(template='plotly_white')

    fig_removal_rate = px.line(
        dff,
        x="fiscal_year",
        y="removals_per_1000_children",
        title=f"Removals per 1,000 Children from {county} County",
        labels={
            "fiscal_year": "DFPS Fiscal Year",
            "removals_per_1000_children" : "Removal Rate (per 1,000 Children)"
        }
    )
    fig_removal_rate.update_layout(template='plotly_white')

    fig_victim_rate = px.line(
        dff,
        x='fiscal_year',
        y='victims_per_1000_children',
        title=f"Confirmed Victims per 1,000 Children in {county} County",
        labels={"fiscal_year": "DFPS Fiscal Year",
                "victims_per_1000_children": "Confirmed Victim Rate (per 1,000 Children)"
        }
    )
    fig_victim_rate.update_layout(template='plotly_white')

    return fig_pop, fig_removal_rate, fig_victim_rate

# Run app
if __name__== "__main__":
    app.run(debug=True)