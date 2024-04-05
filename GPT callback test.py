import dash
from dash import *
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample data
data = pd.DataFrame({
    'State': ['New York', 'California', 'Texas', 'Florida', 'Illinois'],
    'Value': [10, 15, 8, 12, 7]
})

# Dash app
app = dash.Dash(__name__)

# Choropleth map
fig_map = px.choropleth(data, locations='State', locationmode='USA-states', color='Value', scope='usa')

# DataTable
table = html.Div([
    dash_table.DataTable(
        id='datatable',
        columns=[{'name': col, 'id': col} for col in data.columns],
        data=data.to_dict('records')
    )
])

# Layout
app.layout = html.Div([
    dcc.Graph(figure=fig_map, id='choropleth-map'),
    table
])

# Callback to update DataTable based on selected state
@app.callback(
    Output('datatable', 'data'),
    [Input('choropleth-map', 'clickData')]
)
def update_table(selected_state):
    if selected_state is None:
        # If no state is selected, return the original data
        return data.to_dict('records')

    clicked_state = selected_state['points'][0]['location']
    sorted_data = data[data['State'] == clicked_state].sort_values(by='Value', ascending=False)
    
    return sorted_data.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)