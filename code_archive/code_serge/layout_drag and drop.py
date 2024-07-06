from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data reading:
data_path = 'daten_prototyp_Antw_Ber.csv'
df = pd.read_csv(data_path, sep=';')

# App Layout:
app.layout = html.Div([
    html.H1("Eye-Tracking Data Analysis"),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-image-upload'),
    dbc.Row([
        dbc.Col(html.Img(id='img', style={'width': '100%', 'height': 'auto'}), width=6),
        dbc.Col(dcc.Graph(id="graph2"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph3"), width=6),
        dbc.Col(dcc.Graph(id="graph4"), width=6)
    ])
])

def parse_contents(contents, filename):
    return html.Div([
        html.H5(filename),
        html.Img(src=contents, style={'width': '100%', 'height': 'auto'})
    ])

@app.callback(
    Output('output-image-upload', 'children'),
    Input('upload-image', 'contents'),
    prevent_initial_call=True
)
def update_output(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')

        # Decode the base64 string
        decoded = base64.b64decode(content_string)

        return parse_contents(contents, 'Uploaded Image')

if __name__ == '__main__':
    app.run_server(debug=False)

