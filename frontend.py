import pandas as pd
import plotly.graph_objects as go 
from dash import * 
import dash_bootstrap_components as dbc
import csv
import pandas as pd
import pandas as pd

#######################################################################################################
#Generate Map Data from API Pull 
#To pull new API Data run backend.py 
#######################################################################################################
nationwideNumbers = ['Nationwide','USA',0,0]
states = [
['Nationwide','USA',0,0],
['Alabama','AL',0,0],
['Alaska','AK',0,0],
['Arizona','AZ',0,0],
['Arkansas','AR',0,0],
['California','CA',0,0],
['Colorado','CO',0,0],
['Connecticut','CT',0,0],
['Delaware','DE',0,0],
['District of Columbia','DC',0,0],
['Florida','FL',0,0],
['Georgia','GA',0,0],
['Hawaii','HI',0,0],
['Idaho','ID',0,0],
['Illinois','IL',0,0],
['Indiana','IN',0,0],
['Iowa','IA',0,0],
['Kansas','KS',0,0],
['Kentucky','KY',0,0],
['Louisiana','LA',0,0],
['Maine','ME',0,0],
['Maryland','MD',0,0],
['Massachusetts','MA',0,0],
['Michigan','MI',0,0],
['Minnesota','MN',0,0],
['Mississippi','MS',0,0],
['Missouri','MO',0,0],
['Montana','MT',0,0],
['Nebraska','Ne',0,0],
['Nevada','NV',0,0],
['Missouri','MO',0,0],
['Montana','MT',0,0],
['Nebraska','NE',0,0],
['Nevada','NV',0,0],
['New Hampshire','NH',0,0],
['New Jersey','NJ',0,0],
['New Mexico','NM',0,0],
['New York','NY',0,0],
['North Carolina','NC',0,0],
['North Dakota','ND',0,0],
['Ohio','OH',0,0],
['Oklahoma','OK',0,0],
['Oregon','OR',0,0],
['Pennsylvania','PA',0,0],
['Puerto Rico','PR',0,0],
['Rhode Island','RI',0,0],
['South Carolina','SC',0,0],
['South Dakota','SD',0,0],
['Tennessee','TN',0,0],
['Texas','TX',0,0],
['Utah','UT',0,0],
['Vermont','VT',0,0],
['Virginia','VA',0,0],
['Washington','WA',0,0],
['West Virginia','WV',0,0],
['Wisconsin','WI',0,0],
['Wyoming','WY',0,0],]

global nationWideActive
global nationWideClosed

nationWideActive = 0
nationWideClosed = 0

activeStates = []
closedStates = []

def convert():
    with open("./hi.json") as f:
        temp = pd.read_json(f)
        temp.to_csv("hicsv.csv", index=False)
convert() 

def getStateIndex(state): 
  for i in range(len(states)):
    if str(state).strip() == str(states[i][0]):
      return i
  print(state)
  return -1
  
def readCSV():
    with open("hicsv.csv", encoding = "utf8") as df:
        temp = pd.read_csv(df)
        types = temp.loc[:, "field_recall_type"]
        stateList = temp.loc[:, "field_states"]
        print(len(types))
        print(len(stateList))
        floatEntries = 0
        zeroLength = 0
        for i in range(len(types)):
            if types[i] == 'Active Recall':
                if type(stateList[i]) != float:
                  statesGot = stateList[i].split(",")
                  if len(statesGot) == 0: 
                    zeroLength += 1
                  for j in range(len(statesGot)):
                      index = getStateIndex(statesGot[j])
                      states[index][2] += 1          
                else:         
                    floatEntries += 1
                    continue
            elif types[i] == 'Closed Recall':
              if type(stateList[i]) != float:
                statesGot = stateList[i].split(",")
                if len(statesGot) == 0: 
                  zeroLength += 1
                for j in range(len(statesGot)):
                    index = getStateIndex(statesGot[j])
                    states[index][3] += 1          
              else:         
                  floatEntries += 1
                  continue
        print(floatEntries)
        print(zeroLength)
        
def writeActive():
    nationWideActive = 0
    for x in activeStates:
        if type(x) != float:
            if "Nationwide" == x[0]:
                nationWideActive += 1
            else:
                tempNumb = 0
                for i in range(len(states)):
                    stateName = states[i][0]
                    if stateName in x:
                        states[i][2] += 1
    return nationWideActive

def writeClosed():
    nationWideClosed = 0
    for x in closedStates:
        if type(x) != float:
            if "Nationwide" == x[0]:
                nationWideClosed += 1
            else:
                tempNumb = 0
                for i in range(len(states)):
                    stateName = states[i][0]
                    if stateName in x:
                        states[i][3] += 1
    return nationWideClosed

readCSV()
nwNumbers = states[0]
del states[0]
    
with open('map.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["State", "Postal", "Active", "Closed"])
    writer.writerows(states)
outcsv.close

df = pd.read_csv('map.csv')
na = nwNumbers[2]
nc = nwNumbers[3]

#######################################################################################################
#Generate Front End via Plotly and Dash
#######################################################################################################

activeMap = go.Figure(data=go.Choropleth(
    locations=df['Postal'], # Spatial coordinates
    z = df['Active'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Sunsetdark',
))
activeMap.update_layout(
    title_text = 'Active Recalls per State<br><sup>Active Nationwide Recalls: '+str(na),
    geo_scope='usa', # limite map scope to USA
)
closedMap = go.Figure(data=go.Choropleth(
    locations=df['Postal'], # Spatial coordinates
    z = df['Closed'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Emrld',
))
closedMap.update_layout(
    title_text = 'Closed Recalls per State<br><sup>Closed Nationwide Recalls: '+str(nc),
    geo_scope='usa', # limite map scope to USA
)

df = pd.read_csv("data_file.csv")
data = pd.read_csv("recallsPerState.csv")
colors = {
    'safeShelfGreen': '#00bf63'
}

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
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

######################################
#Credit to Roger Allen
#US State Abbrev
#https://gist.github.com/rogerallen/1583593
######################################
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
        stateName = str(abbrev_to_us_state.get(clicked_state))
        stateNationwide = stateName + "|Nationwide" 
        adf = df.loc[df['Recall Status'] == "Active Recall"]
        sdf = adf[adf['States'].str.contains(stateNationwide) == True]
        return sdf.to_dict('records')
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
        stateName = str(abbrev_to_us_state.get(clicked_state))
        stateNationwide = stateName + "|Nationwide" 
        adf = df.loc[df['Recall Status'] == "Closed Recall"]
        sdf = adf[adf['States'].str.contains(stateNationwide) == True]
        return sdf.to_dict('records')
    
@callback(
    Output('datatable', 'data', allow_duplicate=True),
    Input('clearClosed', 'n_clicks'),
    prevent_initial_call=True
)
def reset_graph(n_clicks):
    return df.to_dict('records')
if __name__ == '__main__':
    app.run(debug=True)