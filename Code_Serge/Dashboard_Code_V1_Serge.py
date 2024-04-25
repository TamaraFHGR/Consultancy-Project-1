from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_table

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data reading:
data_Antw_Ber = 'daten_prototyp_Antw_Ber.csv'

# CSV-Datei einlesen
data = pd.read_csv(data_Antw_Ber,
                   sep=';',
                   usecols=['Timestamp', 'StimuliName', 'FixationIndex', 'FixationDuration',
                            'MappedFixationPointX', 'MappedFixationPointY', 'user', 'description'])

df = pd.DataFrame(data)

total_fixation_duration = df['FixationDuration'].sum()
total_fixations = len(df)
average_fixation_duration = df['FixationDuration'].mean()

# App Layout:
app.layout = html.Div([
    html.H1("Eye-Tracking Data Analysis"),
    dbc.Row([
        dbc.Col(html.Img(src='assets/01_Antwerpen_S1_Color.jpg',
                         style={'width': '100%', 'height': 'auto'}),
                width=6),
        dbc.Col(dcc.Graph(id="graph2"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph3"), width=6),
        dbc.Col(html.Div(id="table-container"), width=6)
    ])
])

@app.callback(
    Output('graph2', 'figure'),
    [Input('graph2', 'id')]
)
def update_graph2(_):
    fig = px.scatter(df, x='MappedFixationPointX', y='MappedFixationPointY',
                     size='FixationDuration',
                     title='Gaze Plot')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
    )
    return fig

@app.callback(
    Output('table-container', 'children'),
    [Input('graph3', 'id')]
)
def update_graph3(_):
    table = dash_table.DataTable(
        id='table',
        columns=[
            {"name": "KPI", "id": "KPI"},
            {"name": "Farbe", "id": "Farbe"},
            {"name": "Schwarz/Weiss", "id": "Schwarz/Weiss"}
        ],
        data=[
            {"KPI": "Dauer", "Farbe": f"{total_fixation_duration} ms", "Schwarz/Weiss": ""},
            {"KPI": "Anzahl Fixation", "Farbe": total_fixations, "Schwarz/Weiss": ""},
            {"KPI": "Durchschnittliche Fixation Dauer", "Farbe": f"{average_fixation_duration} ms", "Schwarz/Weiss": ""}
        ],
        style_cell={'textAlign': 'left','minWidth': '0px', 'maxWidth': '180px'},  # Left-align text in cells
        style_header={
            'backgroundColor': 'rgb(7, 0, 97)',  # Set header background color
            'color': 'rgb(255,255,255)'  # Set header text color to white
        },
        style_data_conditional=[
            {
                'if': {'row_index': 0},  # Style the second row
                'backgroundColor': 'rgb(115, 121, 181)',  # Set background color
                'color': 'black'  # Set text color
            },
            {
                'if': {'row_index': 1},  # Style the third row
                'backgroundColor': 'rgb(115, 121, 181)',  # Set background color
                'color': 'black'  # Set text color
            },
            {
                'if': {'row_index': 2},  # Style the fourth row
                'backgroundColor': 'rgb(115, 121, 181)',  # Set background color
                'color': 'black'  # Set text color
            }
        ]
    )
    return table

if __name__ == '__main__':
    app.run_server(debug=False)
