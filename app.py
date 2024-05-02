from dash import Dash, dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import glob

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

"""
-----------------------------------------------------------------------------------------

Data Import and Preparation
"""
# Data reading:
data_path = 'assets/all_fixation_data_cleaned_up.csv'
df = pd.read_csv(data_path, sep=';')
"""
-----------------------------------------------------------------------------------------

KPI Calculation:
total_fixation_duration = df['FixationDuration'].sum()
fixation_duration_color = df[df['description'] == 'color']['FixationDuration'].sum()
fixation_duration_grey = df[df['description'] == 'gray']['FixationDuration'].sum()

total_fixations = len(df)
total_fixations_color = len(df[df['description'] == 'color'])
total_fixations_grey = len(df[df['description'] == 'gray'])

average_fixation_duration = df['FixationDuration'].mean()
average_fixation_duration_color = df[df['description'] == 'color']['FixationDuration'].mean()
average_fixation_duration_grey = df[df['description'] == 'gray']['FixationDuration'].mean()
-----------------------------------------------------------------------------------------

Definition of Dash Layout
"""
app.layout = html.Div([
    html.Div(
        id='header-area',
        children=[
            html.H1('Analysis of Eye-Tracking Data'),
            html.P("This Dashboard enables the visual analysis of eye-tracking data based on metro maps of different cities.")

        ]
    ),
    html.Div(
        id='dropdown-area',
        children=[
            #html.H2("Please select a City-Map"),
            html.P("Please select a City-Map:"),
            dcc.Dropdown(
                id='dropdown_city',
                options=[{'label': city, 'value': city} for city in sorted(df['City'].unique())]
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
            ), width=6),
        dbc.Col(
            dcc.Graph(id="scatter_plot_grey"),
            width=6)
    ])
])
"""
-----------------------------------------------------------------------------------------

Bild-Anzeige (Zeile 1, Spalte 1)
"""
@app.callback(
    Output('city_image', 'src'),
    [Input('dropdown_city', 'value')]
)
def update_image(selected_city):
    if selected_city:
        return f'assets/{selected_city}.jpg'
    return None
"""
-----------------------------------------------------------------------------------------

Scatter_plot_color (Zeile 1, Spalte 2):
"""
def get_image_path_color(selected_city):
    file_pattern_color = f'assets/*_{selected_city}_Color.jpg'
    matching_files = glob.glob(file_pattern_color)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('scatter_plot_color', 'figure'),
    [Input('dropdown_city', 'value')]
)
def update_scatter_plot_color(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['City'] == selected_city) & (df['description'] == 'color')]
        fig = px.scatter(filtered_df,
                         x='MappedFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         title=('Colored Metro Map Observations in ' + selected_city),
                         labels={
                             'MappedFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        image_path_color = get_image_path_color(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_color,
                x=0,
                sizex=filtered_df['MappedFixationPointX'].max(),
                y=filtered_df['MappedFixationPointY'].max(),
                sizey=filtered_df['MappedFixationPointY'].max(),
                xref="x",
                yref="y",
                sizing = "stretch",
                opacity=0.6,
                layer="below"
            )
        )
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
        )
        return fig
    else:
        return px.scatter(title='Please select a city to view data')
"""
-----------------------------------------------------------------------------------------

# KPI Tabelle (Zeile 2, Spalte 1):
"""
@app.callback(
    Output('table_container', 'children'),
    [Input('dropdown_city', 'value')]
)
def update_table_container(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['City'] == selected_city)]

        # Calculations based on filtered DataFrame
        fixation_duration_color = filtered_df[filtered_df['description'] == 'color']['FixationDuration'].sum()
        fixation_duration_grey = filtered_df[filtered_df['description'] == 'gray']['FixationDuration'].sum()
        total_fixations_color = filtered_df[filtered_df['description'] == 'color'].shape[0]
        #total_fixations_color = len(filtered_df[df['description'] == 'color'])
        total_fixations_grey = filtered_df[filtered_df['description'] == 'gray'].shape[0]
        #total_fixations_grey = len(filtered_df[df['description'] == 'gray'])
        average_fixation_duration_color = filtered_df[df['description'] == 'color']['FixationDuration'].mean()
        #average_fixation_duration_color = fixation_duration_color / total_fixations_color if total_fixations_color else 0
        average_fixation_duration_grey = filtered_df[df['description'] == 'gray']['FixationDuration'].mean()
        #average_fixation_duration_grey = fixation_duration_grey / total_fixations_grey if total_fixations_grey else 0

        table = dash_table.DataTable(
            id='table_container',
            columns=[
                {"name": "KPI", "id": "KPI"},
                {"name": "Color Map", "id": "Color"},
                {"name": "Greyscale Map", "id": "Greyscale"}
            ],
            data=[
                {"KPI": "Fixation Duration", "Color": f"{round(fixation_duration_color,2)} ms", "Greyscale": f"{round(fixation_duration_grey,2)} ms"},
                {"KPI": "Number of Fixation-Points", "Color": total_fixations_color, "Greyscale": total_fixations_grey},
                {"KPI": "Average Fixation-Duration", "Color": f"{round(average_fixation_duration_color,2)} ms", "Greyscale": f"{round(average_fixation_duration_grey,2)} ms"}
            ],
            style_cell={
                'textAlign': 'left',
                'minWidth': '0px',
                'maxWidth': '180px'
                },  # Left-align text in cells
            style_header={
            'backgroundColor': 'rgb(7, 0, 97)',  # Set header background color
            'color': 'rgb(255,255,255)'  # Set header text color to white
                },
            style_data_conditional=[{
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
    else:
        return "Please select a city to view data"
"""
-----------------------------------------------------------------------------------------

Scatter_plot_grey (Zeile 2, Spalte 2):
"""
def get_image_path_grey(selected_city):
    file_pattern_grey = f'assets/*_{selected_city}_Grey.jpg'
    matching_files = glob.glob(file_pattern_grey)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('scatter_plot_grey', 'figure'),
    [Input('dropdown_city', 'value')]
)
def update_scatter_plot_grey(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['City'] == selected_city) & (df['description'] == 'gray')]
        fig = px.scatter(filtered_df,
                         x='MappedFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         title=('Greyscale Metro Map Observations in ' + selected_city),
                         labels={
                             'MappedFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        image_path_grey = get_image_path_grey(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_grey,
                x=0,
                sizex=filtered_df['MappedFixationPointX'].max(),
                y=filtered_df['MappedFixationPointY'].max(),
                sizey=filtered_df['MappedFixationPointY'].max(),
                xref="x",
                yref="y",
                sizing="stretch",
                opacity=0.6,
                layer="below"
            )
        )
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
        )
        return fig
    else:
        return px.scatter(title='Please select a city to view data')



if __name__ == '__main__':
    app.run_server(debug=True)
