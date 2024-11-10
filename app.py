import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load data
df = pd.read_csv('full_grouped.csv')
total = df['Confirmed'].sum()
deaths = df['Deaths'].sum()
active = df['Active'].sum()
recovered = df['Recovered'].sum()

# Dropdown options
options = [
    {'label': 'Total', 'value': 'total'},
    {'label': 'Deaths', 'value': 'deaths'},
    {'label': 'Active', 'value': 'active'},
    {'label': 'Recovered', 'value': 'recovered'}
]

# External CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-HCw98/SFnGE8fJT3GXwE0ngsV72t27NXFoaoApmYm81iuXoPkF0JwJ8ERdknLPM0',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Apply global background style directly in app layout
app.layout = html.Div(style={'background-color': '#000000', 'padding': '20px'}, children=[

    html.H1('COVID-19', style={'text-align': 'center', 'color': 'white'}),

    html.Div([  # Single row with four columns side-by-side
        html.Div([
            html.Div([
                html.H3("Total Cases", style={'color': 'red'}),
                html.H4(total, style={'color': 'red'})
            ], className='card-body')
        ], className='card bg-info col-md-3', style={'border-radius': '8px', 'height': '150px', 'margin': '10px'}),

        html.Div([
            html.Div([
                html.H3("Active Cases", style={'color': 'blue'}),
                html.H4(active, style={'color': 'blue'})
            ], className='card-body')
        ], className='card bg-warning col-md-3', style={'border-radius': '8px', 'height': '150px', 'margin': '10px'}),

        html.Div([
            html.Div([
                html.H3("Deaths", style={'color': 'green'}),
                html.H4(deaths, style={'color': 'green'})
            ], className='card-body')
        ], className='card bg-success col-md-3', style={'border-radius': '8px', 'height': '150px', 'margin': '10px'}),

        html.Div([
            html.Div([
                html.H3("Recoveries", style={'color': 'yellow'}),
                html.H4(recovered, style={'color': 'yellow'})
            ], className='card-body')
        ], className='card bg-danger col-md-3', style={'border-radius': '8px', 'height': '150px', 'margin': '10px'})
    ], className='row', style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id='picker', options=options, value='total'),
                dcc.Graph(id='bar')
            ], className='card-body')
        ], className='card')
    ], className='row')
])

@app.callback(Output('bar', 'figure'), Input('picker', 'value'))
                                                                            #If more than one input add Input(#same)
def update_graph(type):

    if type=='ALL':

       pbar = df['Country/Region'].value_counts().reset_index()
       return {'data' : [go.Bar(x=pbar['Country/Region'], y=pbar['count'])],
               'layout' : go.Layout(title='Country Total Count')}

    else:

        npat = df[df['current'] == type]
        #New logic can be added
        pbar = df['Country/Region'].value_counts().reset_index()
        return {'data': [go.Bar(x=pbar['Country/Region'], y=pbar['count'])],
                'layout': go.Layout(title='Country Total Count')}


if __name__ == '__main__':
    app.run_server(debug=True)
