import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # or plotly.express as px
from collections import OrderedDict
from dash import * 
import dash_bootstrap_components as dbc
import csv
from pathlib import Path
import flask

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

df = pd.read_csv("data_file.csv")
data = pd.read_csv("recallsPerState.csv")

colors = {
    'safeShelfGreen': '#00bf63'
}

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
df = df.iloc[:,0:4]

app.layout = html.Div(
    dbc.Container([
        dbc.Row( 
            dbc.Col(
            html.Div(children=[html.H1(children='SafeShelf: Your Recall Buddy',)],
            style={ 'textAlign': 'left', 'color': colors['safeShelfGreen']}),
                )
        ),
        
        dbc.Row([
                dbc.Col(
                    html.Div(children=['USDA FSIS Recalls',
                        dash_table.DataTable(
                            style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'text-align': 'center',
                            },
                            id="datatable",
                            data=df.to_dict('records'),
                            columns=[{'id': c, 'name': c, } for c in df.columns],
                            fixed_rows={'headers': True},
                            style_table={'height': 500},  # defaults to 500
                            sort_action="native",
                            filter_action="native",
                            page_action='none',
                            filter_options={"placeholder_text": "Search by..."},
                            sort_mode="single",
                            column_selectable="single",
                            style_cell={
                            'minWidth': '100px', 'width': '150px', 'maxWidth': '350px'}
                            )]), 
                            width={'size':6},
                    ),
                
                dbc.Col(
                    dbc.Tabs([
                        dbc.Tab(label="ActiveMap", tab_id="Active Recall Map", children=[
                            dcc.Graph(figure=activeMap, id='active-map'),
                            html.Div([
                                dbc.Button('View All States', id='clearActive', color="primary"),
                            ],  style={'margin-bottom': '10px',
                                'textAlign':'center',
                                'width': '220px',
                                'margin':'auto'}
                            )
                            ]),
                        dbc.Tab(label="ClosedMap", tab_id="Closed Recall Map", children=[
                            dcc.Graph(figure=closedMap, id='closed-map'),
                            html.Div([
                                dbc.Button('View All States', id='clearClosed', color="primary"),
                            ],  style={'margin-bottom': '10px',
                                'textAlign':'center',
                                'width': '220px',
                                'margin':'auto'}
                            )
                            ]),
                        ]), width={'size':6},
                    ),
            ]),
    ]), style={'width': '100%', 'display': 'block'},
)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

@app.callback(
    Output('datatable', 'data', allow_duplicate=True),
    Input('active-map', 'clickData'),
    prevent_initial_call=True
)
def update_active_table(active_select):
    if active_select is None:
        return df.to_dict('records')
    else:
        clicked_state = active_select['points'][0]['location']
        sdf = data[data['State'] == clicked_state]
        stateName = abbrev_to_us_state.get(clicked_state)
        filtered_df = df.loc[df['States'] == stateName]
        return filtered_df.to_dict('records')
    
@callback(
    Output('datatable', 'data', allow_duplicate=True),
    Input('clearActive', 'n_clicks'),
    prevent_initial_call=True
)
def reset_graph(n_clicks):
    return df.to_dict('records')

@callback(
    Output('datatable', 'data', allow_duplicate=True),
    [Input('closed-map', 'clickData')],
    prevent_initial_call=True
)  
def update_closed_table(closed_select):
    if closed_select is None:
        return df.to_dict('records')
    else:
        clicked_state = closed_select['points'][0]['location']
        sdf = data[data['State'] == clicked_state]
        stateName = abbrev_to_us_state.get(clicked_state)
        filtered_df = df.loc[df['States'] == stateName]
        return filtered_df.to_dict('records')
    
@callback(
    Output('datatable', 'data', allow_duplicate=True),
    Input('clearClosed', 'n_clicks'),
    prevent_initial_call=True
)
def reset_graph(n_clicks):
    return df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)