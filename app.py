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
        dbc.Col(html.Img(src='assets/01_Antwerpen_S1_Color.png',
                         style={'width': '100%', 'height': 'auto'}),
                width=6),
        dbc.Col(dcc.Graph(id="graph2"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph3"), width=6),
        dbc.Col(dcc.Graph(id="graph4"), width=6)
    ])
])

@app.callback(
    Output('graph1', 'figure'),
    Input('graph1', 'id')
)

def update_graph1(_):
    #Bild einlesen:
    img_path = 'assets/01_Antwerpen_S1_Color.png'
    img = Image.open(img_path)
    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=df['MappedFixationPointX'].max(),
            sizey=df['MappedFixationPointY'].max(),
            sizing="stretch",
            opacity=1.0,
            layer="below"
        )
    )
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    return fig


    #img_path = 'assets/01_Antwerpen_S1_Color.jpg'
    #fig = Image.open(img_path)
    #return fig

@app.callback(
    Output('graph2', 'figure'),
    Input('graph2', 'id')
)

def update_graph2(_):
    fig = px.scatter(df, x='MappedFixationPointX', y='MappedFixationPointY',
                     size='FixationDuration',
                     title='Gaze Plot')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
