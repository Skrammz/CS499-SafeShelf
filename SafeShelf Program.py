import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # or plotly.express as px
from collections import OrderedDict
from dash import * 
import dash_bootstrap_components as dbc
import csv
from pathlib import Path

csv = 'recallsPerState.csv'
df = pd.read_csv(csv)

na = df['Nationwide Active'].astype(float)
nationwideActive = int(na.sum())

activeMap = go.Figure(data=go.Choropleth(
    locations=df['Postal'], # Spatial coordinates
    z = df['Active'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Sunsetdark',
))
activeMap.update_layout(
    title_text = 'Active Recalls per State<br><sup>Active Nationwide Recalls: '+str(nationwideActive),
    geo_scope='usa', # limite map scope to USA
)

nc = df['Nationwide Closed'].astype(float)
nationwideClosed = int(nc.sum())

closedMap = go.Figure(data=go.Choropleth(
    locations=df['Postal'], # Spatial coordinates
    z = df['Closed'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Emrld',
))
closedMap.update_layout(
    title_text = 'Closed Recalls per State<br><sup>Closed Nationwide Recalls: '+str(nationwideClosed),
    geo_scope='usa', # limite map scope to USA
)

data = pd.read_csv('recallsPerState.csv')
recallTable = pd.DataFrame(OrderedDict([(name, col_data) for (name, col_data) in data.items()]))


colors = {
    'safeShelfGreen': '#00bf63'
}

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

df = df.iloc[:,0:4]

app.layout = html.Div(
    dbc.Container([
        dbc.Row( 
            dbc.Col(
            html.Div(children=[html.H1(children='SafeShelf: Your Recall Buddy')],
            style={ 'textAlign': 'left', 'color': colors['safeShelfGreen']}),
                )
            ),
        dbc.Row([
                dbc.Col(
                    html.Div(children=['USDA FSIS Recalls',
                        dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in df.columns],
                            fixed_rows={'headers': True},
                            style_table={'height': 500}  # defaults to 500
                            )               
                        ]), width={'size':6},
                    ),
                
                dbc.Col(
                    dbc.Tabs([
                        dbc.Tab(label="ActiveMap", tab_id="Active Recall Map", children=[
                            dcc.Graph(figure=activeMap)
                            ]),
                        dbc.Tab(label="ClosedMap", tab_id="Closed Recall Map", children=[
                            dcc.Graph(figure=closedMap)
                            ]),
                        ]), width={'size':6},
                    ),
            ]
        )
    ]), style={'width': '100%', 'display': 'block'},
)
    
if __name__ == '__main__':
    app.run(debug=True)