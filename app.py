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
data_path = 'assets/all_fixation_data_cleaned_up_3.csv'
df = pd.read_csv(data_path, sep=';')

# Add "Task Duration in sec" (per User and Stimulus) to df:
task_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].sum().reset_index()
task_duration['FixationDuration'] = task_duration['FixationDuration'] / 1000
df = pd.merge(df, task_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_aggregated'))

# Add "Average Fixation Duration in sec" (per User and Stimulus) to df:
avg_fix_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].mean().reset_index()
avg_fix_duration['FixationDuration'] = avg_fix_duration['FixationDuration'] / 1000
df = pd.merge(df, avg_fix_duration, on=['CityMap', 'description'], suffixes=('', '_avg'))

#print(df)

"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""
app.layout = html.Div([
    html.Div([                          # Spalte 1
        html.Div(
            id='header-area',                   # Spalte 1 / Container 1
            children=[
                html.H1('Analysis of Eye-Tracking Data'),
                html.H2('This dashboard enables the visual analysis of eye-tracking data,'
                   ' based on metro maps of different cities.')
            ]
        ),
        html.Div(
            id='selection-area',                # Spalte 1 / Container 2
            children=[
                html.H3('To gain more insight on the analysis results of a specific city, please select a visualization type and a city map.'),
                html.P('Please select a type of visualization:'),
                dcc.RadioItems(
                    id='radio_visualization',
                    options=[{'label': i, 'value': i} for i in ['No Selection (landing page)', 'Gaze-Plot', 'Heat-Map']],
                    value='No Selection (landing page)'),
                html.P('Please select a city map:'),
                dcc.Dropdown(
                    id='dropdown_city',
                    options=[{'label': city, 'value': city} for city in sorted(df['CityMap'].unique())],
                    value=None)
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
                        style={'width': 'auto', 'height': 'auto'}),
                     dcc.Graph(
                         id='gaze_plot_color'),
                     dcc.Graph(
                         id='heat_map_color'),
                     dcc.Graph(
                         id='box_task_duration'),
                     #html.P('Select a User'),
                     #dcc.Dropdown(
                     #    id='dropdown_user_color',
                     #    options=[{'label': user, 'value': user} for user in
                     #             sorted(df[df['description'] == 'color']['user'].unique())],
                     #    value=None),
                     #html.P('Select a range of Task Duration'),
                     # dcc.RangeSlider(
                     #      id='range_slider_color',
                     #      min=1,
                     #      max=50,
                     #      step=None,
                     #      value=[
                     #          df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                     #          df[df['description'] == 'color']['FixationDuration_aggregated'].max()]),
                 ]),
        html.Div(
            id='grey_plot_area',
            children=[                     # Spalte 2 / Container 2 (grey)
                html.Img(
                    id='city_image_grey',
                    style={'width': 'auto', 'height': 'auto'}),
                dcc.Graph(
                    id='gaze_plot_grey'),
                dcc.Graph(
                    id='heat_map_grey'),
                dcc.Graph(
                    id='box_avg_fixation_duration'),
                # html.P('Select a User'),
                # dcc.Dropdown(
                #     id='dropdown_user_grey',
                #     options=[{'label': user, 'value': user} for user in
                #              sorted(df[df['description'] == 'grey']['user'].unique())],
                # ),
                # html.P('Select a range of Task Duration'),
                # dcc.RangeSlider(
                #     id='range_slider_grey',
                #     min=1,
                #     max=50,
                #     step=None,
                #     value=[
                #         df[df['description'] == 'grey']['FixationDuration_aggregated'].min(),
                #         df[df['description'] == 'grey']['FixationDuration_aggregated'].max()],)
            ])
    ], className='six columns')
], className='row')

"""
-----------------------------------------------------------------------------------------
Section 3:
Define Plot-Selection Area
"""

@app.callback(
    [Output('color_plot_area', 'children'),
     (Output('grey_plot_area', 'children'))],
    [Input('radio_visualization', 'value')]
)

def update_plot_area(visualization_type):
    if visualization_type == 'Gaze-Plot':
        return [
             dcc.Graph(id='gaze_plot_color'),
             dcc.Graph(id='gaze_plot_grey')
        ]
    elif visualization_type == 'Heat-Map':
        return [
             dcc.Graph(id='heat_map_color'),
             dcc.Graph(id='heat_map_grey')
        ]
    elif visualization_type == 'No Selection (landing page)':
         return [
             dcc.Graph(id='box_task_duration'),
             dcc.Graph(id='box_avg_fixation_duration')
        ]
"""
-----------------------------------------------------------------------------------------
Section 4:
Define KPI-Area
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

        # 4. Average Fixation Duration (seconds):
        avg_fixation_duration_color = filtered_df[filtered_df['description'] == 'color']['FixationDuration'].mean() / 1000
        avg_fixation_duration_grey = filtered_df[filtered_df['description'] == 'grey']['FixationDuration'].mean() / 1000

        table = dash_table.DataTable(
            columns=[
                {"name": "KPI", "id": "KPI"},
                {"name": "Color Map", "id": "color"},
                {"name": "Greyscale Map", "id": "greyscale"}
            ],
            data=[
                {"KPI": "Average Task Duration", "color": f"{round(avg_task_color,2)} sec", "greyscale": f"{round(avg_task_grey,2)} sec"},
                {"KPI": "Number of Fixation-Points", "color": fixation_points_color, "greyscale": fixation_points_grey},
                {"KPI": "Average Saccade Length", "color": round(avg_saccade_color,2), "greyscale": round(avg_saccade_grey,2)},
                {"KPI": "Average Fixation Duration", "color": f"{round(avg_fixation_duration_color,2)} sec", "greyscale": f"{round(avg_fixation_duration_grey,2)} sec"}
            ],
            style_cell={'className': 'cell-style'},
            style_header={'className': 'header-style'},
            style_data_conditional=[
                {'if': {'row_index': 'even'},
                 'className': 'data-row-even'},
                {'if': {'row_index': 'odd'},
                 'className': 'data-row-odd'}]
        )

        return table
    else:
        return "Please select a city map to view related KPI data"

"""
-----------------------------------------------------------------------------------------
Section 5:
Define Scatter-Plot Color
"""
def get_image_path_color(selected_city):
    file_pattern_color = f'assets/*_{selected_city}_Color.jpg'
    matching_files = glob.glob(file_pattern_color)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('gaze_plot_color', 'figure'),
    [Input('dropdown_city', 'value')])
def update_scatter_plot_color(selected_city):
    if selected_city:
        # Define a color map for users
        unique_users = df['user'].dropna().unique()
        colors = px.colors.qualitative.Plotly  # Use Plotly's qualitative color scale
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(unique_users)}

        filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'color')]

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='NormalizedXFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         title=('Color Map Observations in ' + selected_city),
                         labels={
                             'NormalizedXFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        fig.update_xaxes(range=[0, 1651])
        fig.update_yaxes(range=[0, 1200])

        # Add line traces for each user
        for user in filtered_df['user'].unique():
            user_df = filtered_df[filtered_df['user'] == user]
            fig.add_trace(
                go.Scatter(
                    x=user_df['NormalizedXFixationPointX'],
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
                x=154.5,    # x-Position des Bildes in Pixel
                sizex=1805.5,  # None setzt die Originalbreite
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # None setzt die Originalhöhe
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
Section 6:
Define Scatter-Plot Grey
"""
def get_image_path_grey(selected_city):
    file_pattern_grey = f'assets/*_{selected_city}_Grey.jpg'
    matching_files = glob.glob(file_pattern_grey)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('gaze_plot_grey', 'figure'),
    [Input('dropdown_city', 'value')])

def update_scatter_plot_grey(selected_city):
    if selected_city:
        # Define a color map for users
        unique_users = df['user'].dropna().unique()
        colors = px.colors.qualitative.Plotly
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(unique_users)}

        # Filter and sort data based on the selected filters
        filtered_df = df[
            (df['CityMap'] == selected_city) &
            (df['description'] == 'grey')]

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='NormalizedXFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         title=('Greyscale Map Observations in ' + selected_city),
                         labels={
                             'NormalizedXFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        fig.update_xaxes(range=[0, 1960])
        fig.update_yaxes(range=[0, 1200])

        # Add line traces for each user
        for user in filtered_df['user'].unique():
            user_df = filtered_df[filtered_df['user'] == user]
            fig.add_trace(
                go.Scatter(
                    x=user_df['NormalizedXFixationPointX'],
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
                x=154.5,    # x-Position des Bildes in Pixe
                sizex=1960,  # Originalbreite
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # None setzt die Originalhöhe
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
Section 7:
Define Density Heat-Map Color
"""
@app.callback(
    Output('heat_map_color', 'figure'),
    [Input('dropdown_city', 'value')])

def update_heatmap_color(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'color')]

        fig = px.density_contour(filtered_df,
                                 x='NormalizedXFixationPointX',
                                 y='MappedFixationPointY',
                                 nbinsx=20,
                                 nbinsy=20,
                                 title=('Color Map Observations in ' + selected_city),)

        fig.update_xaxes(range=[0, 1960])
        fig.update_yaxes(range=[0, 1200])

        # Add Background Image
        image_path_color = get_image_path_color(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_color,
                x=154.5,    # x-Position des Bildes in Pixel
                sizex=1805.5,  # None setzt die Originalbreite
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # None setzt die Originalhöhe
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
Section 8:
Define Density Heat-Map Grey
"""
@app.callback(
    Output('heat_map_grey', 'figure'),
    [Input('dropdown_city', 'value')])

def update_heatmap_grey(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'grey')]

        fig = px.density_contour(filtered_df,
                                 x='NormalizedXFixationPointX',
                                 y='MappedFixationPointY',
                                 nbinsx=20,
                                 nbinsy=20,
                                 title=('Greyscale Map Observations in ' + selected_city),)

        fig.update_xaxes(range=[0, 1960])
        fig.update_yaxes(range=[0, 1200])

        # Add Background Image
        image_path_grey = get_image_path_grey(selected_city)
        fig.add_layout_image(
            dict(
                source=image_path_grey,
                x=154.5,    # x-Position des Bildes in Pixel
                sizex=1805.5,  # None setzt die Originalbreite
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # None setzt die Originalhöhe
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
Section 9:
Define Box-Plot "Task Duration" (Distribution of Task Duration (A-B) per User, Color, City)
"""

@app.callback(
    Output('box_task_duration', 'figure'),
    [Input('radio_visualization', 'value')])
def update_box_plot_task_duration(visualization_type):
    if visualization_type == 'No Selection (landing page)':
        city_order = df['City'].sort_values().unique().tolist()
        fig = px.box(df,
                     x='FixationDuration_aggregated',
                     y='City',
                     #points='outliers',
                     color='description',
                     boxmode='overlay',
                     category_orders={'City': city_order},
                     title='Distribution of Task Duration per City',
                     color_discrete_map = {
                         'color': 'skyblue',
                         'grey': 'lightgrey'},
                     labels = {'FixationDuration_aggregated': 'Task Duration [sec.]',
                               'City': '',
                               'description': 'Map Type'})

        fig.update_traces(marker=dict(size=5), line=dict(width=1.0))

        fig.update_yaxes(dtick=1,)

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)')  # Set paper color to transparent

        return fig

"""
-----------------------------------------------------------------------------------------
Section 10:
Define Box-Plot "Average Fixation Duration" (Distribution of Average Fixation Duration per User, Color, City)
"""

@app.callback(
    Output('box_avg_fixation_duration', 'figure'),
    [Input('radio_visualization', 'value')])
def update_box_plot_avg_fixation_duration(visualization_type):
    if visualization_type == 'No Selection (landing page)':
        city_order = df['City'].sort_values().unique().tolist()

        fig = px.box(df,
                      x='FixationDuration_avg',
                      y='City',
                      #points='outliers',
                      color='description',
                      boxmode='overlay',
                      category_orders={'City': city_order},
                      title='Distribution of Average Fixation Duration per City',
                      color_discrete_map={
                          'color': 'skyblue',
                          'grey': 'lightgrey'},
                      labels={'FixationDuration_avg': 'Average Fixation Duration [sec.]',
                              'City': '',
                              'description': 'Map Type'})

        fig.update_traces(marker=dict(size=5), line=dict(width=1.0))

        fig.update_yaxes(dtick=1,)

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)')  # Set paper color to transparent

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
