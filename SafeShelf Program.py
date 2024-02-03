import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash, html, dcc
import csv
from pathlib import Path

csv = 'recallsPerState.csv'
df = pd.read_csv(csv, sep=',')

activeMap = go.Figure(data=go.Choropleth(
    locations=df['Postal'], # Spatial coordinates
    z = df['Active'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Sunsetdark',
    colorbar_title = "Active Recalls per State",
))
activeMap.update_layout(
    title_text = 'Active Recalls per State',
    geo_scope='usa', # limite map scope to USA
)

closedMap = go.Figure(data=go.Choropleth(
    locations=df['Postal'], # Spatial coordinates
    z = df['Closed'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Emrld',
    colorbar_title = "Closed Recalls per State",
))
closedMap.update_layout(
    title_text = 'Closed Recalls per State',
    geo_scope='usa', # limite map scope to USA
)

df = pd.read_csv(csv)
def generate_table(dataframe, max_rows=51):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='SafeShelf: Your Recall Buddy', style={'textAlign':'left'}),
    html.H4(children='USDA FSIS Recalls'),
    generate_table(df),
    dcc.Graph(figure=activeMap, responsive=True), #responsive refers to size
    dcc.Graph(figure=closedMap, responsive=True)  #responsive refers to size
])

if __name__ == '__main__':
    app.run(debug=True)
