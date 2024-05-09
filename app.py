from dash import Dash, dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import glob
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

"""
-----------------------------------------------------------------------------------------
Section 1:
Data Import and Preparation
"""
# Data reading:
data_path = 'assets/all_fixation_data_cleaned_up_2.csv'
df = pd.read_csv(data_path, sep=';')
# Task Duration in sec per User and Stimulus:
task_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].sum().reset_index()
task_duration['FixationDuration'] = task_duration['FixationDuration'] / 1000
df = pd.merge(df, task_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_aggregated'))
#print(df)

"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""
app.layout = html.Div([
    # 1. Spalte mit drei Zeilen
    html.Div([
        html.Div(
            id='header-area',
            children=[
                # Zeile 1 - Header-Area:
                html.H1('Analysis of Eye-Tracking Data'),
                html.H2('This dashboard enables the visual analysis of eye-tracking data,'
                   ' based on metro maps of different European cities.')
            ]
        ),
        html.Div(
            id='selection-area',
            children=[
                # Zeile 2 - Selection-Area:
                html.P('Please select a City-Map:'),
                dcc.Dropdown(
                    id='dropdown_city',
                    options=[{'label': city, 'value': city} for city in sorted(df['CityMap'].unique())]
                                ),
                html.P('Choose a Type of Visualization:'),
                dcc.RadioItems(
                    id='radio_visualization',
                    options=[
                        {'label': 'Gaze-Plot', 'value': 'Gaze-Plot'},
                        {'label': 'Heat-Map', 'value': 'Heat-Map'}]
                )
            ]
        ),
        html.Div(
            id='kpi-area',
            children=[
                # Zeile 3 - KPI-Area:
                html.P('Statistical Key Performance Indicators:'),
                dcc.Tab(
                    id='table_container'
                )]
            )
    ], className='six columns'),
    # 2. Spalte mit zwei Zeilen
    html.Div([
        html.Div(
            id='color_plot_area',
            children=[
                # Zeile 1 - Color-Plot-Area:
                html.Img(
                    id='city_image_color',
                    style={'width': '90%', 'height': 'auto%'}),
                dcc.Graph(
                    id='plot_color_1'),
                html.P('Select a User'),
                dcc.Dropdown(
                    id='dropdown_user_color_1',
                    options=[{'label': user, 'value': user} for user in
                             sorted(df[df['description'] == 'color']['user'].unique())],
                ),
                html.P('Select a range of Task Duration'),
                dcc.RangeSlider(
                    id='range_slider_color_1',
                    min=1,
                    max=50,
                    step=None,
                    value=[
                        df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                        df[df['description'] == 'color']['FixationDuration_aggregated'].max()],
                ),
                dcc.Graph(
                    id='plot_color_2'),
                html.P('Select a User'),
                dcc.Dropdown(
                    id='dropdown_user_color_2',
                    options=[{'label': user, 'value': user} for user in
                             sorted(df[df['description'] == 'color']['user'].unique())],
                ),
                html.P('Select a range of Task Duration'),
                dcc.RangeSlider(
                    id='range_slider_color_2',
                    min=1,
                    max=50,
                    step=None,
                    value=[
                        df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                        df[df['description'] == 'color']['FixationDuration_aggregated'].max()],
                )
            ]),
        html.Div(
            id='grey_plot_area',
            children=[
                # Zeile 2 - Grey-Plot-Area:
                html.Img(
                    id='city_image_grey',
                    style={'width': '90%', 'height': 'auto%'}),
                dcc.Graph(
                    id='plot_grey_1'),
                html.P('Select a User'),
                dcc.Dropdown(
                    id='dropdown_user_grey',
                    options=[{'label': user, 'value': user} for user in
                             sorted(df[df['description'] == 'grey']['user'].unique())],
                ),
                html.P('Select a range of Task Duration'),
                dcc.RangeSlider(
                    id='range_slider_grey',
                    min=1,
                    max=50,
                    step=None,
                    value=[
                        df[df['description'] == 'grey']['FixationDuration_aggregated'].min(),
                        df[df['description'] == 'grey']['FixationDuration_aggregated'].max()],
                )
            ])
    ], className='six columns')
], className='row')

"""
-----------------------------------------------------------------------------------------
Section 3: Define Plot-Selection Area:
"""

@app.callback(
    Output('color_plot_area', 'children'),
    [Input('radio_visualization', 'value')]
)

def update_plot_area(visualization_type):
    if visualization_type == 'Gaze-Plot':
        return [
            html.Img(
                id='city_image_color',
                style={'width': '90%', 'height': 'auto%'}),
            dcc.Graph(
                id='plot_color_1'),
            html.P('Select a User'),
            dcc.Dropdown(
                id='dropdown_user_color_1',
                options=[{'label': user, 'value': user} for user in
                         sorted(df[df['description'] == 'color']['user'].unique())],
            ),
            html.P('Select a range of Task Duration'),
            dcc.RangeSlider(
                id='range_slider_color_1',
                min=1,
                max=50,
                step=None,
                value=[
                    df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                    df[df['description'] == 'color']['FixationDuration_aggregated'].max()],
            )
        ]
    else:
        return [
            html.Img(
                id='city_image_color',
                style={'width': '90%', 'height': 'auto%'}),
            dcc.Graph(
                id='plot_color_2'),
            html.P('Select a User'),
            dcc.Dropdown(
                id='dropdown_user_color_2',
                options=[{'label': user, 'value': user} for user in
                         sorted(df[df['description'] == 'color']['user'].unique())],
            ),
            html.P('Select a range of Task Duration'),
            dcc.RangeSlider(
                id='range_slider_color_2',
                min=1,
                max=50,
                step=None,
                value=[
                    df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                    df[df['description'] == 'color']['FixationDuration_aggregated'].max()],
            )
        ]

"""
-----------------------------------------------------------------------------------------
Section 4: Define KPI-Area:
"""
@app.callback(
    Output('table_container', 'children'),
    [Input('dropdown_city', 'value')]
)
def update_table_container(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['CityMap'] == selected_city)]

        # 1. Average Task Duration (seconds):
        # Sum of FixationDuration per Color / Number of Users per Color
        avg_task_color = (filtered_df[filtered_df['description'] == 'color']['FixationDuration'].sum() / filtered_df[filtered_df['description'] == 'color']['user'].nunique()) / 1000
        avg_task_grey = (filtered_df[filtered_df['description'] == 'grey']['FixationDuration'].sum() / filtered_df[filtered_df['description'] == 'grey']['user'].nunique()) / 1000

        # 2. Number of Fixation-Points (without unit):
        fixation_points_color = filtered_df[filtered_df['description'] == 'color'].shape[0]
        fixation_points_grey = filtered_df[filtered_df['description'] == 'grey'].shape[0]

        # 3. Average Saccade Length (without unit):
        # Lenght of the movement between two fixation points
        avg_saccade_color = filtered_df[filtered_df['description'] == 'color']['SaccadeLength'].mean()
        avg_saccade_grey = filtered_df[filtered_df['description'] == 'grey']['SaccadeLength'].mean()

        table = dash_table.DataTable(
            columns=[
                {"name": "KPI", "id": "KPI"},
                {"name": "Color Map", "id": "color"},
                {"name": "Greyscale Map", "id": "greyscale"}
            ],
            data=[
                {"KPI": "Average Task Duration", "color": f"{round(avg_task_color,2)} sec", "greyscale": f"{round(avg_task_grey,2)} sec"},
                {"KPI": "Number of Fixation-Points", "color": fixation_points_color, "greyscale": fixation_points_grey},
                {"KPI": "Average Saccade Length", "color": round(avg_saccade_color,2), "greyscale": round(avg_saccade_grey,2)}
            ],
            style_cell={
                'textAlign': 'left',
                'minWidth': '0px',
                'maxWidth': '180px'
                },  # Left-align text in cells
            style_header={
            'backgroundColor': '#000000',  # Set header background color
            'color': '#FFFFFF'  # Set header text color to white
                },
            style_data_conditional=[{
                'if': {'row_index': 0},  # Style the second row
                    'backgroundColor': '#E6E6E6',  # Set background color
                    'color': '#000000'  # Set text color
                },
                {
                'if': {'row_index': 1},  # Style the third row
                    'backgroundColor': '#CBCBCB',  # Set background color
                    'color': '#000000'  # Set text color
                },
                {
                'if': {'row_index': 2},  # Style the fourth row
                    'backgroundColor': '#E6E6E6',  # Set background color
                    'color': '#000000'  # Set text color
                }
            ]
        )
        return table
    else:
        return "Please select a city to view data"

"""
-----------------------------------------------------------------------------------------
Section 5: Define Scatter-Plot Color:
"""
def get_image_path_color(selected_city):
    file_pattern_color = f'assets/*_{selected_city}_Color.jpg'
    matching_files = glob.glob(file_pattern_color)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('plot_color_1', 'figure'),
    [Input('dropdown_city', 'value'),
     Input('dropdown_user_color_1', 'value'),
     Input('range_slider_color_1', 'value')]
)
def update_scatter_plot_color(selected_city, selected_user, slider_value_color):
    if selected_city:
        # Define a color map for users
        unique_users = df['user'].dropna().unique()
        colors = px.colors.qualitative.Plotly  # Use Plotly's qualitative color scale

        # Create a dictionary to map each user to a specific color
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(unique_users)}

        # Check if a user is selected or the "All" option is chosen
        if selected_user == 'All' or not selected_user:
            user_filter = df['user'].notnull()  # If 'All' users or no user selected, include all non-null user entries
        else:
            user_filter = (df['user'] == selected_user)  # Specific user is selected

        # Filter and sort data based on the selected filters
        filtered_df = df[
            (df['CityMap'] == selected_city) &
            (df['description'] == 'color') &
            user_filter &
            (df['FixationDuration_aggregated'] >= slider_value_color[0]) &
            (df['FixationDuration_aggregated'] <= slider_value_color[1])
            ].sort_values(by='FixationIndex')

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='MappedFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         title=('Color Map Observations in ' + selected_city),
                         labels={
                             'MappedFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        fig.update_xaxes(range=[0, 1650])
        fig.update_yaxes(range=[0, 1200])

        # Add line traces for each user
        for user in filtered_df['user'].unique():
            user_df = filtered_df[filtered_df['user'] == user]
            fig.add_trace(
                go.Scatter(
                    x=user_df['MappedFixationPointX'],
                    y=user_df['MappedFixationPointY'],
                    mode='lines',
                    line=dict(width=2, color=color_map[user]),
                    name=f"Scanpath for {user}"
                )
            )

        # Add Background Image
        image_path_color = get_image_path_color(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_color,
                x=0,    # x-Position des Bildes in Pixel
                sizex=1650,  # Breite des Bildes in Pixel
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # Höhe des Bildes in Pixel
                xref="x",
                yref="y",
                sizing="contain",  # Das Bild wird so skaliert, dass es komplett sichtbar ist, ohne gestreckt zu werden
                opacity=0.6,
                layer="below"
            )
        )
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
        )
        return fig
    else:
        return px.scatter(title='Please select a city to view data')

"""
-----------------------------------------------------------------------------------------
Section 6: Define Scatter-Plot Grey:
"""
def get_image_path_grey(selected_city):
    file_pattern_grey = f'assets/*_{selected_city}_Grey.jpg'
    matching_files = glob.glob(file_pattern_grey)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('plot_grey_1', 'figure'),
    [Input('dropdown_city', 'value'),
     Input('dropdown_user_grey', 'value'),
     Input('range_slider_grey', 'value')]
)
def update_scatter_plot_grey(selected_city, selected_user, slider_value_color):
    if selected_city:
        # Define a color map for users
        unique_users = df['user'].dropna().unique()
        colors = px.colors.qualitative.Plotly  # Use Plotly's qualitative color scale

        # Create a dictionary to map each user to a specific color
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(unique_users)}

        # Check if a user is selected or the "All" option is chosen
        if selected_user == 'All' or not selected_user:
            user_filter = df['user'].notnull()  # If 'All' users or no user selected, include all non-null user entries
        else:
            user_filter = (df['user'] == selected_user)  # Specific user is selected

        # Filter and sort data based on the selected filters
        filtered_df = df[
            (df['CityMap'] == selected_city) &
            (df['description'] == 'grey') &
            user_filter &
            (df['FixationDuration_aggregated'] >= slider_value_color[0]) &
            (df['FixationDuration_aggregated'] <= slider_value_color[1])
            ].sort_values(by='FixationIndex')

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='MappedFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         title=('Greyscale Map Observations in ' + selected_city),
                         labels={
                             'MappedFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        fig.update_xaxes(range=[0, 1650])
        fig.update_yaxes(range=[0, 1200])

        # Add line traces for each user
        for user in filtered_df['user'].unique():
            user_df = filtered_df[filtered_df['user'] == user]
            fig.add_trace(
                go.Scatter(
                    x=user_df['MappedFixationPointX'],
                    y=user_df['MappedFixationPointY'],
                    mode='lines',
                    line=dict(width=2, color=color_map[user]),
                    name=f"Scanpath for {user}"
                )
            )

        # Add Background Image
        image_path_grey = get_image_path_grey(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_grey,
                x=0,    # x-Position des Bildes in Pixel
                sizex=1650,  # Breite des Bildes in Pixel
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # Höhe des Bildes in Pixel
                xref="x",
                yref="y",
                sizing="contain",  # Das Bild wird so skaliert, dass es komplett sichtbar ist, ohne gestreckt zu werden
                opacity=0.6,
                layer="below"
            )
        )
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
        )
        return fig
    else:
        return px.scatter(title='Please select a city to view data')

"""
-----------------------------------------------------------------------------------------
Section 7: Define Density Heat-Map Color:
"""
@app.callback(
    Output('plot_color_2', 'figure'),
    [Input('dropdown_city', 'value'),
     Input('dropdown_user_color_2', 'value'),
     Input('range_slider_color_2', 'value')]
)

def update_heatmap_color(selected_city, selected_user, slider_value_color):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'color')]

        # Check if a user is selected or the "All" option is chosen
        if selected_user == 'All' or not selected_user:
            user_filter = df['user'].notnull()  # If 'All' users or no user selected, include all non-null user entries
        else:
            user_filter = (df['user'] == selected_user)  # Specific user is selected

        # Filter and sort data based on the selected filters
        filtered_df = filtered_df[
            (df['CityMap'] == selected_city) &
            (df['description'] == 'color') &
            user_filter &
            (df['FixationDuration_aggregated'] >= slider_value_color[0]) &
            (df['FixationDuration_aggregated'] <= slider_value_color[1])
            ].sort_values(by='FixationIndex')

        fig = px.density_contour(filtered_df,
                                 x='MappedFixationPointX',
                                 y='MappedFixationPointY',
                                 nbinsx=20,
                                 nbinsy=20,
                                 title=('Color Map Observations in ' + selected_city),)

        # Add Background Image
        image_path_color = get_image_path_color(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_color,
                x=0,    # x-Position des Bildes in Pixel
                sizex=1650,  # Breite des Bildes in Pixel
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # Höhe des Bildes in Pixel
                xref="x",
                yref="y",
                sizing="contain",  # Das Bild wird so skaliert, dass es komplett sichtbar ist, ohne gestreckt zu werden
                opacity=0.6,
                layer="below"
            )
        )
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
        )
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
