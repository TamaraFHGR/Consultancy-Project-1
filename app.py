from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data reading:
data_path = 'assets/daten_prototyp_Antw_p1_color.csv'
df = pd.read_csv(data_path, sep=';')

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
            dcc.Graph(id="kpi_table"),
            width=6),
        dbc.Col(
            dcc.Graph(id="scatter_plot_grey"),
            width=6)
    ])
])
# Scatter_plot_color:
@app.callback(
    Output('scatter_plot_color','figure'),
    [Input('dropdown_city', 'value')]
)
def update_scatter_plot_color(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[df['City'] == selected_city]
        fig = px.scatter(
            filtered_df, x='MappedFixationPointX', y='MappedFixationPointY',
            size='FixationDuration',
            title='Scatter-Plot color Map')
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
                opacity=0.5,
                layer="below")
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

if __name__ == '__main__':
    app.run_server(debug=True)
