from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from code_split.import_00_data_loader import load_and_process_data
from code_split.import_01_table_container import update_table_container
from code_split.import_02_gaze_plot_color import update_gaze_plot_color
from code_split.import_03_heat_map_color import update_heat_map_color
from code_split.import_04_gaze_plot_grey import update_gaze_plot_grey
from code_split.import_05_heat_map_grey import update_heat_map_grey

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

data_path = '../assets/all_fixation_data_cleaned_up_2.csv'
df = load_and_process_data(data_path)

"""
-----------------------------------------------------------------------------------------
Section 1:
Definition of Dash Layout
"""
app.layout = html.Div([
    html.Div([                          # Spalte 1
        html.Div(
            id='header-area',                   # Spalte 1 / Container 1
            children=[
                html.H1('Analysis of Eye-Tracking Data'),
                html.H2('This dashboard enables the visual analysis of eye-tracking data,'
                   ' based on metro maps of different European cities.')
            ]
        ),
        html.Div(
            id='selection-area',                # Spalte 1 / Container 2
            children=[
                html.P('Please select a City-Map:'),
                dcc.Dropdown(
                    id='dropdown_city',
                    options=[{'label': city, 'value': city} for city in sorted(df['CityMap'].unique())],
                    value='Antwerpen_S1'),
                html.P('Choose a Type of Visualization:'),
                dcc.RadioItems(
                    id='radio_visualization',
                    options=[{'label': 'Gaze-Plot', 'value': 'Gaze-Plot'},
                             {'label': 'Heat-Map', 'value': 'Heat-Map'}],
                    value='Gaze-Plot')
            ]
        ),
        html.Div(
            id='kpi-area',                      # Spalte 1 / Container 3
            children=[
                html.P('Statistical Key Performance Indicators:'),
                dcc.Tab(
                    id='table_container'
                )]
            )
    ], className='six columns'),
    html.Div([                          # Spalte 2
        html.Div(id='color_plot_area',
                 children=[                     # Spalte 2 / Container 1 (color)
                     html.Img(
                        id='city_image_color',
                        style={'width': '90%', 'height': 'auto'}),
                     dcc.Graph(
                         id='gaze_plot_color'),
                     dcc.Graph(
                         id='heat_map_color'),
                     html.P('Select a User'),
                     dcc.Dropdown(
                         id='dropdown_user_color',
                         options=[{'label': user, 'value': user} for user in sorted(df[df['description'] == 'color']['user'].unique())],
                         value='P1'),
                     html.P('Select a range of Task Duration'),
                     dcc.RangeSlider(
                          id='range_slider_color',
                          min=1,
                          max=50,
                          step=None,
                          value=[
                              df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                              df[df['description'] == 'color']['FixationDuration_aggregated'].max()]),
                 ]),
        html.Div(id='grey_plot_area',
                 children=[                     # Spalte 2 / Container 2 (grey)
                     html.Img(
                         id='city_image_grey',
                         style={'width': '90%', 'height': 'auto'}),
                     dcc.Graph(
                         id='gaze_plot_grey'),
                     dcc.Graph(
                         id='heat_map_grey'),
                     html.P('Select a User'),
                     dcc.Dropdown(
                         id='dropdown_user_grey',
                         options=[{'label': user, 'value': user} for user in
                                  sorted(df[df['description'] == 'grey']['user'].unique())],
                         value='P1'),
                     html.P('Select a range of Task Duration'),
                     dcc.RangeSlider(
                         id='range_slider_grey',
                         min=1,
                         max=50,
                         step=None,
                         value=[
                             df[df['description'] == 'grey']['FixationDuration_aggregated'].min(),
                             df[df['description'] == 'grey']['FixationDuration_aggregated'].max()]),
                 ])
    ], className='six columns')
], className='row')

"""
-----------------------------------------------------------------------------------------
Section 2:
Define KPI-Area
"""
@app.callback(
    Output('table_container', 'children'),
    [Input('dropdown_city', 'value')])

def update_table_container_callback(selected_city):
    if selected_city is None:
        return "Please select a city to view data"
    return update_table_container(selected_city)

"""
-----------------------------------------------------------------------------------------
Section 3:
Define Color-Plot Area
"""
@app.callback(
    Output('gaze_plot_color', 'figure'),
    [Input('dropdown_city', 'value')])

def update_gaze_plot_color_callback(selected_city):
    if selected_city is None:
        return px.scatter(title='Please select a city to view data')
    return update_gaze_plot_color(selected_city)

@app.callback(
    Output('heat_map_color', 'figure'),
    [Input('dropdown_city', 'value')])

def update_heat_map_color_callback(selected_city):
    if selected_city is None:
        return px.scatter(title='Please select a city to view data')
    return update_heat_map_color(selected_city)

"""
-----------------------------------------------------------------------------------------
Section 4:
Define Scatter-Plot Grey
"""

@app.callback(
    Output('gaze_plot_grey', 'figure'),
    [Input('dropdown_city', 'value')])

def update_gaze_plot_grey_callback(selected_city):
    if selected_city is None:
        return px.scatter(title='Please select a city to view data')
    return update_gaze_plot_grey(selected_city)

@app.callback(
    Output('heat_map_grey', 'figure'),
    [Input('dropdown_city', 'value')])

def update_heat_map_grey_callback(selected_city):
    if selected_city is None:
        return px.scatter(title='Please select a city to view data')
    return update_heat_map_grey(selected_city)

"""
-----------------------------------------------------------------------------------------
Section 5:
Define Visualization Type
"""

@app.callback(
    Output('color_plot_area', 'children'),
    [Input('radio_visualization', 'value')]
)

def update_color_plot_area_callback(visualization_type):
    if visualization_type == 'Gaze-Plot':
        return [
            dcc.Graph(id='gaze_plot_color', style={'display': 'block'}),
            dcc.Graph(id='heat_map_color', style={'display': 'none'})
        ]
    elif visualization_type == 'Heat-Map':
        return [
            dcc.Graph(id='gaze_plot_color', style={'display': 'none'}),
            dcc.Graph(id='heat_map_color', style={'display': 'block'})
        ]

@app.callback(
    Output('grey_plot_area', 'children'),
    [Input('radio_visualization', 'value')]
)

def update_grey_plot_area_callback(visualization_type):
    if visualization_type == 'Gaze-Plot':
        return [
            dcc.Graph(id='gaze_plot_grey', style={'display': 'block'}),
            dcc.Graph(id='heat_map_grey', style={'display': 'none'})
        ]
    else:
        return [
            dcc.Graph(id='gaze_plot_grey', style={'display': 'none'}),
            dcc.Graph(id='heat_map_grey', style={'display': 'block'})
        ]


if __name__ == '__main__':
    app.run_server(debug=True)