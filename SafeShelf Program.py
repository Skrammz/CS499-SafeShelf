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
                            id="datatable",
                            data=df.to_dict('records'),
                            columns=[{'id': c, 'name': c, } for c in df.columns],
                            fixed_rows={'headers': True},
                            style_table={'height': 500},  # defaults to 500
                            sort_action="native",
                            filter_action="native",
                            filter_options={"placeholder_text": "Search by..."},
                            sort_mode="single",
                            column_selectable="single",
                            style_cell={
                            'minWidth': '80px', 'width': '100px', 'maxWidth': '140px'}
                            )]), 
                            width={'size':6},
                    ),
                
                dbc.Col(
                    dbc.Tabs([
                        dbc.Tab(label="ActiveMap", tab_id="Active Recall Map", children=[
                            dcc.Graph(figure=activeMap, id='active-map'),
                            html.Button('Clear State', id='clearActive')
                            ]),
                        dbc.Tab(label="ClosedMap", tab_id="Closed Recall Map", children=[
                            dcc.Graph(figure=closedMap, id='closed-map'),
                            html.Button('Clear State', id='clearClosed')
                            ]),
                        ]), width={'size':6},
                    ),
            ]
        )
    ]), style={'width': '100%', 'display': 'block'},
)

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
        sdf = data[data['Postal'] == clicked_state]
        return sdf.to_dict('records')
    
@app.callback(
    Output('datatable', 'data'),
    Input('clearActive', 'n_clicks'),
)
def reset_graph(n_clicks):
    return df.to_dict('records')

@app.callback(
    Output('datatable', 'data'),
    [Input('closed-map', 'clickData')]
)  
def update_closed_table(closed_select):
    if closed_select is None:
        return df.to_dict('records')
    else:
        clicked_state = closed_select['points'][0]['location']
        sdf = data[data['Postal'] == clicked_state]
        return sdf.to_dict('records')
    
@callback(
    Output('datatable', 'data'),
    Input('clearClosed', 'n_clicks'),
)
def reset_graph(n_clicks):
    return df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)