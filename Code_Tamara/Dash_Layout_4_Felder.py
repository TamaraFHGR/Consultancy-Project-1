from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data reading:
data_path = 'daten_prototyp_Antw_p1_color.csv'
df = pd.read_csv(data_path, sep=';')

# App Layout:
app.layout = html.Div([
    html.H1("Eye-Tracking Data Analysis"),
    dbc.Row([
        dbc.Col([
            html.Label("Select a color dimension:"),
            dcc.Dropdown(id='color', options=[
                {'label': 'Fixation Duration', 'value': 'FixationDuration'},
                {'label': 'Fixation Index', 'value': 'FixationIndex'}
            ], value='FixationDuration'),
            dcc.Graph(id="graph1")
        ], width=6),
        dbc.Col(dcc.Graph(id="graph2"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph3"), width=6),
        dbc.Col(dcc.Graph(id="graph4"), width=6)
    ])
])

# Callback for Graph 1 - Image:
@app.callback(
    Output("graph1", "figure"),
    Input("color", "value")
)
def update_graph1(color):
    #Bild einlesen:
    img_path = '01_Antwerpen_S1_Color.jpg'
    img = Image.open(img_path)

    return fig



# Callback for Graph 2:
@app.callback(
    Output("graph2", "figure"),
    Input("color", "value")
)
def update_graph2(color):
    fig = px.scatter(df, x='MappedFixationPointX', y='MappedFixationPointY',
                     size='FixationDuration', color=color,
                     title='Gaze Plot')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
