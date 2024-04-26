from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data reading:
data_path = 'assets/daten_prototyp_Antw_p1_color.csv'
df = pd.read_csv(data_path, sep=';')

total_fixation_duration = df['FixationDuration'].sum()
total_fixations = len(df)
average_fixation_duration = df['FixationDuration'].mean()

# App Layout:
app.layout = html.Div([
    html.Div(
        id='header-area',
        children=[
            html.H1('Eye-Tracking Data Analysis'),
            html.P("This Dashboard is designed for the visualization of eye-tracking data.")
        ]
    ),
    html.Div(
        id='dropdown-area',
        children=[
            html.H2("Select a City-Map to be displayed:"),
            html.P("This dropdown allows you to select the City to be analysed."),
            dcc.Dropdown(
                id='dropdown_city',
                options=[{'label': city, 'value': city} for city in df['City'].unique()]
            ),
        ]
    ),
    # Zeile 1:
    dbc.Row([
        dbc.Col(
            html.Img(
                id='city_image',
                style={'width': '100%', 'height': 'auto'}),
            width=6),
        dbc.Col(
            dcc.Graph(id="scatter_plot_color"),
            width=6)
    ]),
    # Zeile 2:
    dbc.Row([
        dbc.Col(
            html.Div(
                id="table_container"
            ),width=6),
        dbc.Col(
            dcc.Graph(id="scatter_plot_grey"),
            width=6)
    ])
])


# Scatter_plot_color:
@app.callback(
    Output('scatter_plot_color', 'figure'),
    [Input('dropdown_city', 'value')]
)
def update_scatter_plot_color(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[df['City'] == selected_city]
        fig = px.scatter(df, x='MappedFixationPointX', y='MappedFixationPointY',
                         size='FixationDuration',
                         title='Gaze Plot')
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
        )
        return fig



        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_df['MappedFixationPointX'],
            y=filtered_df['MappedFixationPointY'],
            mode='markers',
            marker=dict(
                size=filtered_df['FixationDuration']
            )
        ))
        fig.add_layout_image(
            dict(
                source=f'assets/01_{selected_city}_S2_Color.jpg',
                xref="x",
                yref="y",
                x=0,
                y=3,
                sizex=2,
                sizey=2,
                sizing="stretch",
                opacity=1,
                layer="above")
        )
        fig.update_layout(
            template="plotly_white"
        )
        return fig

    return px.scatter(title='Select a city to see the data')


@app.callback(
    Output('city_image', 'src'),
    [Input('dropdown_city', 'value')]
)
def update_image(selected_city):
    if selected_city:
        return f'assets/01_{selected_city}_S2_Color.jpg'
    return None

@app.callback(
    Output('table_container', 'children'),
    [Input('table_container', 'id')]
)
def update_table_container(_):
    table = dash_table.DataTable(
        id='table_container',
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
    app.run_server(debug=True)
