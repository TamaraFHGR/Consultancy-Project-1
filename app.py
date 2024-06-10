from dash import Dash, dash_table, dcc, html, Input, Output, State, callback_context
from dash_iconify import DashIconify
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
df = pd.merge(df, avg_fix_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_avg'))

#print('task_duration:')
#print(df['FixationDuration_aggregated'])
#print(df['FixationDuration_aggregated'].min)
#print(df['FixationDuration_aggregated'].max)
#print(df)

"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""
app.layout = html.Div([
    # Header and Theme-Mode:
    html.Div([
        html.Div([
            html.H1('Analysis of Eye-Tracking-Data'),],
            #html.H2('This dasboard enables the visual exploration based on different city maps'), ],
            className='header'),
        dcc.Dropdown(
            id='theme_dropdown',
            options=[
                {'label': 'Light Mode', 'value': 'light'},
                {'label': 'Dark Mode', 'value': 'dark'}],
            value='light',
            clearable=False,
            className='theme_dropdown',
        ),
        dcc.Store(id='current_theme', data='light'),
    ], className='first_container'),

    html.Div([
        # Start first column (Input, KPI, Histogram):
        html.Div([
            # Input-Containers:
            html.Div([
                # City Dropdown:
                html.Div([
                    html.H3([
                        DashIconify(icon="vaadin:train", width=16, height=16, style={"margin-right": "12px"}),
                        'Please select a City:']),
                    dcc.Dropdown(
                        id='city_dropdown',
                        options=[{'label': city, 'value': city} for city in sorted(df['CityMap'].unique())],
                        value=None,
                        clearable=True,
                        className='dropdown'),
                ], className='second_container'),

                # Visualization Type Buttons:
                html.Div([
                    html.H3([
                        DashIconify(icon="ion:bar-chart", width=16, height=16, style={"margin-right": "12px"}),
                        'Please choose a Type of Visualization:']),
                    html.Div([
                        html.Button('Boxplot', id='default_viz', n_clicks=0, className='viz_button'),
                        html.Button('Heat Map', id='heat_map', n_clicks=0, className='viz_button'),
                        html.Button('Gaze Plot', id='gaze_plot', n_clicks=0, className='viz_button'),
                    ], id='button_viz_type', className='button_viz_type'),
                    dcc.Store(id='active-button', data='Boxplot'),
                    html.Div(id='output-section'),
                ], className='third_container'),
            ], className='input_container'),

            # Output-Container KPI-Table:
            html.Div([
                html.H3([
                    DashIconify(icon="fluent:arrow-trending-lines-24-filled", width=16, height=16,
                                style={"margin-right": "12px"}),
                    'Statistical Key Performance Indicators:']),
                html.Div(id='table_container')
            ], className='fourth_container'),

            # Output-Container Histogram:
            html.Div([
                html.H3([
                    DashIconify(icon="humbleicons:eye", width=16, height=16,
                                style={"margin-right": "12px"}),
                    'Distribution of Task Duration:']),
                dcc.Graph(id='hist_taskduration', style={"height": "200px"}),
            ], className='seventh_container'),
        ], className='first_column'),

        # Start second column (Color Map):
        html.Div([
            # Output-Container Color Plot:
            html.Div([
                html.Img(
                    id='city_image_color'),
                dcc.Graph(id='gaze_plot_color', style={"height": "300px", "width": "200px"}),
                dcc.Graph(id='heat_map_color', style={"height": "300px", "width": "200px"}),
                dcc.Dropdown(id='dropdown_user_color', multi=True),
                # dcc.RangeSlider(id='range_slider_color',
                #                 min=1,
                #                 max=20,
                #                 step=0.1,
                #                 value=[1, 20]),
                dcc.Graph(id='box_task_duration')
            ], id='color_plot_area', className='fifth_container'),
        ], className='second_column'),

        # Start third column (Grey Map):
        html.Div([
            # Output-Container Grey Plot:
            html.Div([
                html.Img(
                    id='city_image_grey'),
                dcc.Graph(id='gaze_plot_grey', style={"height": "300px", "width": "200px"}),
                dcc.Graph(id='heat_map_grey', style={"height": "300px", "width": "200px"}),
                dcc.Dropdown(id='dropdown_user_grey', multi=True),
                # dcc.RangeSlider(id='range_slider_grey',
                #                 min=1,
                #                 max=20,
                #                 step=0.1,
                #                 value=[1, 20]),
                dcc.Graph(id='box_avg_fix_duration'),
            ],  id='grey_plot_area', className='sixth_container'),
        ], className='third_column'),
    ], className='dash_container'),
], id='page_content', className='light_theme')

"""
-----------------------------------------------------------------------------------------
Section 3:
Definition of active Viz-Button and Output-Section (based on active Viz-Type)
"""

#1 - Define and keep active button:
@app.callback(
    [Output('default_viz', 'className'),
     Output('heat_map', 'className'),
     Output('gaze_plot', 'className'),
     Output('active-button', 'data')],
    [Input('default_viz', 'n_clicks'),
     Input('heat_map', 'n_clicks'),
     Input('gaze_plot', 'n_clicks')],
    [State('active-button', 'data')]
)

def update_active_button(btn1, btn2, btn3, active_btn):
    ctx = callback_context
    if not ctx.triggered:
        return ['viz_button active' if active_btn == 'default_viz' else 'viz_button',
                'viz_button active' if active_btn == 'heat_map' else 'viz_button',
                'viz_button active' if active_btn == 'gaze_plot' else 'viz_button',
                active_btn]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return ['viz_button active' if button_id == 'default_viz' else 'viz_button',
                'viz_button active' if button_id == 'heat_map' else 'viz_button',
                'viz_button active' if button_id == 'gaze_plot' else 'viz_button',
                button_id]

#2 - Update output and plot area based on active button:
@app.callback(
    Output('output-section', 'children'),
    Input('active-button', 'data')
)
def update_output(active_button):
    if active_button == 'default_viz':
        return ''
    elif active_button == 'heat_map':
        return ''
    elif active_button == 'gaze_plot':
        return ''
    else:
        return ''

@app.callback(
    [Output('color_plot_area', 'children'),
     (Output('grey_plot_area', 'children'))],
    [Input('active-button', 'data')]
)

def update_plot_area(visualization_type):
    if visualization_type == 'gaze_plot':
        return [
            dcc.Graph(id='gaze_plot_color'),
            dcc.Dropdown(id='dropdown_user_color', value=None, multi=True)
        ], [
            dcc.Graph(id='gaze_plot_grey'),
            dcc.Dropdown(id='dropdown_user_grey', value=None, multi=True)
        ]
    elif visualization_type == 'heat_map':
        return [
            dcc.Graph(id='heat_map_color'),
            dcc.Dropdown(id='dropdown_user_color', value=None, multi=True)
        ], [
            dcc.Graph(id='heat_map_grey'),
            dcc.Dropdown(id='dropdown_user_grey', value=None, multi=True)
        ]
    elif visualization_type == 'default_viz':
        return [
            dcc.Graph(id='box_task_duration')
        ], [
            dcc.Graph(id='box_avg_fix_duration')
        ]
    else:
        return ([html.P("No visualization type selected", style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontStyle': 'italic', 'fontSize': '16px', 'margin-top': '10px'})],
                [html.P("No visualization type selected", style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontStyle': 'italic', 'fontSize': '16px', 'margin-top': '10px'})])

#3 - Update Filters in plot area, based on selected city:
@app.callback(
    [Output('dropdown_user_color', 'options'),
     Output('dropdown_user_grey', 'options')],
    [Input('city_dropdown', 'value')]
)
def update_user_dropdowns(selected_city):
    if selected_city:
        # Filter users based on the selected city and description
        filtered_users_color = df[(df['CityMap'] == selected_city) & (df['description'] == 'color')]['user'].unique()
        filtered_users_grey = df[(df['CityMap'] == selected_city) & (df['description'] == 'grey')]['user'].unique()

        # Convert filtered users to dropdown options
        color_options = [{'label': user, 'value': user} for user in filtered_users_color]
        grey_options = [{'label': user, 'value': user} for user in filtered_users_grey]

        return color_options, grey_options

    return [[], []]

"""
-----------------------------------------------------------------------------------------
Section 4:
Definition of Theme-Mode
"""
#1 - Update Theme-Mode based on selected theme:
@app.callback(
    [Output('page_content', 'className'),
     Output('current_theme', 'data')],
    [Input('theme_dropdown', 'value')]
)
def update_theme_mode(theme):
    if theme == 'light':
        return 'light_theme', 'light'
    else:
        return 'dark_theme', 'dark'

#2 - Update Dropdown-Classname based on selected theme:
@app.callback(
    Output('city_dropdown', 'className'),
    [Input('current_theme', 'data')]
)
def update_dropdown_classname(current_theme):
    if current_theme == 'light':
        return 'dropdown light_theme_dropdown'
    else:
        return 'dropdown dark_theme_dropdown'

"""
-----------------------------------------------------------------------------------------
Section 5:
Definition of KPI-Area
"""
@app.callback(
    Output('table_container', 'children'),
    [Input('city_dropdown', 'value')]
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

        return dash_table.DataTable(
        id='kpi_table',
        columns=[
            {"name": "KPI", "id": "KPI"},
            {"name": "Color Map", "id": "color"},
            {"name": "Grey Map", "id": "greyscale"}
        ],
        data=[
            {"KPI": "Avg. Task Duration", "color": f"{round(avg_task_color, 2)} sec",
             "greyscale": f"{round(avg_task_grey, 2)} sec"},
            {"KPI": "No. Fixation-Points", "color": fixation_points_color, "greyscale": fixation_points_grey},
            {"KPI": "Avg. Saccade Length", "color": round(avg_saccade_color, 2),
             "greyscale": round(avg_saccade_grey, 2)},
            {"KPI": "Avg. Fixation Duration", "color": f"{round(avg_fixation_duration_color, 2)} sec",
             "greyscale": f"{round(avg_fixation_duration_grey, 2)} sec"}
        ],
        style_cell={
            'textAlign': 'left',
            'padding': '4px',
            'whiteSpace': 'nowrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'font': 'normal 10px Arial'
        },
        style_header={
            'backgroundColor': '#000000',
            'color': 'white',
            'textAlign': 'left',
            'padding': '4px',
            'font': 'normal 10px Arial'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#E6E6E6',
                'color': 'black',},
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#CBCBCB',
                'color': 'black',},
            {
                'if': {'column_id': 'KPI'},
                'minWidth': '120px', 'maxWidth': '120px',},
            {
                'if': {'column_id': 'color'},
                'minWidth': '60px', 'maxWidth': '60px',},
            {
                'if': {'column_id': 'greyscale'},
                'minWidth': '60px', 'maxWidth': '60px',},
        ]
    )
    else:
        return html.Div("Please select a city map to view related KPI data.", style={'fontSize': '12px', 'fontFamily': 'Arial', 'fontStyle': 'italic'})

"""
-----------------------------------------------------------------------------------------
Section 6:
Definition of Scatter-Plot Color
"""
def get_image_path_color(selected_city):
    file_pattern_color = f'assets/*_{selected_city}_Color.jpg'
    matching_files = glob.glob(file_pattern_color)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('gaze_plot_color', 'figure'),
    [Input('city_dropdown', 'value'),
     Input('dropdown_user_color', 'value'),
     Input('current_theme', 'data')]
)
def update_scatter_plot_color(selected_city, selected_users, current_theme):
    if selected_city:
        # Define a color map for users
        unique_users = df['user'].dropna().unique()
        colors = px.colors.qualitative.Plotly
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(unique_users)}

        # Filter and sort data based on the selected filters (city and user):
        filtered_df = df[
            (df['CityMap'] == selected_city) & (df['description'] == 'color')]

        if selected_users:
            if isinstance(selected_users, str):
                selected_users = [selected_users]
            filtered_df = filtered_df[filtered_df['user'].isin(selected_users)]

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='NormalizedXFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         labels={
                             'NormalizedXFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        fig.update_xaxes(range=[0, 1651],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(range=[0, 1200],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

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
                x=154.5,    # x-Position des Bildes in Pixe
                sizex=1805.5,  # Originalbreite
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # None setzt die Originalhöhe
                xref="x",
                yref="y",
                sizing="contain",  # Das Bild wird so skaliert, dass es komplett sichtbar ist, ohne gestreckt zu werden
                opacity=0.6,
                layer="below"
            )
        )

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            xaxis_title=None,
            yaxis_title=None,
            title={
                'text': f'<b>Color Map Observations in {selected_city}</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color }
            },
            margin=dict(l=0, r=5, t=40, b=5),
            showlegend=False)
        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            title={'text': f"<i>Please select a city to view data<i>.",
                   'y': 0.6,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'font': dict(
                       size=16,
                       color=title_color,
                       family='Arial, sans-serif')},
            showlegend=False,
            margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)

        return fig

"""
-----------------------------------------------------------------------------------------
Section 7:
Definition of Scatter-Plot Grey
"""
def get_image_path_grey(selected_city):
    file_pattern_grey = f'assets/*_{selected_city}_Grey.jpg'
    matching_files = glob.glob(file_pattern_grey)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]

@app.callback(
    Output('gaze_plot_grey', 'figure'),
    [Input('city_dropdown', 'value'),
     Input('dropdown_user_grey', 'value'),
     Input('current_theme', 'data')]
)

def update_scatter_plot_grey(selected_city, selected_users, current_theme):
    if selected_city:
        # Define a color map for users
        unique_users = df['user'].dropna().unique()
        colors = px.colors.qualitative.Plotly
        color_map = {user: colors[i % len(colors)] for i, user in enumerate(unique_users)}

        # Filter and sort data based on the selected filters (city and user):
        filtered_df = df[
            (df['CityMap'] == selected_city) & (df['description'] == 'grey')]

        if selected_users:
            if isinstance(selected_users, str):
                selected_users = [selected_users]
            filtered_df = filtered_df[filtered_df['user'].isin(selected_users)]

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='NormalizedXFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         labels={
                             'NormalizedXFixationPointX': 'X Coordinate',
                             'MappedFixationPointY': 'Y Coordinate',
                             'FixationDuration': 'Duration (ms)'
                         })
        fig.update_xaxes(range=[0, 1651],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(range=[0, 1200],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

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
                sizex=1805.5,  # Originalbreite
                y=1200,    # y-Position des Bildes in Pixel
                sizey=1200,  # None setzt die Originalhöhe
                xref="x",
                yref="y",
                sizing="contain",  # Das Bild wird so skaliert, dass es komplett sichtbar ist, ohne gestreckt zu werden
                opacity=0.6,
                layer="below"
            )
        )

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            xaxis_title=None,
            yaxis_title=None,
            title={
                'text': f'<b>Greyscale Map Observations in {selected_city}</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color }
            },
            margin=dict(l=0, r=5, t=40, b=5),
            showlegend=False)
        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            title={'text': f"<i>Please select a city to view data<i>.",
                   'y': 0.6,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'font': dict(
                       size=16,
                       color=title_color,
                       family='Arial, sans-serif')},
            showlegend=False,
            margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)

        return fig

"""
-----------------------------------------------------------------------------------------
Section 8:
Definition of Density Heat-Map Color
"""
@app.callback(
    Output('heat_map_color', 'figure'),
    [Input('city_dropdown', 'value'),
     Input('dropdown_user_color', 'value'),
     Input('current_theme', 'data')]
)

def update_heatmap_color(selected_city, selected_users, current_theme):
    if selected_city:
        # Filter and sort data based on the selected filters (city and user):
        filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'color')]

        if selected_users:
            if isinstance(selected_users, str):
                selected_users = [selected_users]
            filtered_df = filtered_df[filtered_df['user'].isin(selected_users)]

        fig = px.density_contour(filtered_df,
                                 x='NormalizedXFixationPointX',
                                 y='MappedFixationPointY',
                                 nbinsx=30,
                                 nbinsy=30)

        fig.update_traces(
            contours_showlabels=False,
            contours_coloring="fill",
            line=dict(
                smoothing=1.3,
                color='rgba(0, 0, 0, 0)'  # Set contour line color to transparent
            ),
            colorscale=[
                [0.0, "rgba(0, 128, 0, 0)"],  # Green, but transparent
                [0.2, "rgba(0, 128, 0, 0.5)"],  # Green with some opacity
                [0.4, "rgba(173, 255, 47, 0.6)"],  # Yellow-green with moderate opacity
                [0.6, "rgba(255, 255, 0, 0.7)"],  # Yellow with higher opacity
                [0.8, "rgba(255, 165, 0, 0.8)"],  # Orange with more opacity
                [1.0, "rgba(255, 0, 0, 0.9)"]  # Red with full opacity
            ],
            showscale=False)

        fig.update_xaxes(range=[0, 1651],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(range=[0, 1200],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

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
                opacity=1,
                layer="below"
            )
        )

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            xaxis_title=None,
            yaxis_title=None,
            title={
                'text': f'<b>Color Map Observations in {selected_city}</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            margin=dict(l=0, r=5, t=40, b=5),
            showlegend=False)
        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            title={
                'text': "<i>Please select a city to view data<i>.",
                'y': 0.6,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {
                    'size': 16,
                    'color': title_color,
                    'family': 'Arial, sans-serif'
                }},
            showlegend=False,
            margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)

        return fig

"""
-----------------------------------------------------------------------------------------
Section 9:
Definition of Density Heat-Map Grey
"""
@app.callback(
    Output('heat_map_grey', 'figure'),
    [Input('city_dropdown', 'value'),
     Input('dropdown_user_grey', 'value'),
     Input('current_theme', 'data')]
)

def update_heatmap_grey(selected_city, selected_users, current_theme):
    if selected_city:
        # Filter and sort data based on the selected filters (city and user):
        filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'grey')]

        if selected_users:
            if isinstance(selected_users, str):
                selected_users = [selected_users]
            filtered_df = filtered_df[filtered_df['user'].isin(selected_users)]

        fig = px.density_contour(filtered_df,
                                 x='NormalizedXFixationPointX',
                                 y='MappedFixationPointY',
                                 nbinsx=30,
                                 nbinsy=30)

        fig.update_traces(
            contours_showlabels=False,
            contours_coloring="fill",
            line=dict(
                smoothing=1.3,
                color='rgba(0, 0, 0, 0)'  # Set contour line color to transparent
            ),
            colorscale=[
                [0.0, "rgba(0, 128, 0, 0)"],  # Green, but transparent
                [0.2, "rgba(0, 128, 0, 0.5)"],  # Green with some opacity
                [0.4, "rgba(173, 255, 47, 0.6)"],  # Yellow-green with moderate opacity
                [0.6, "rgba(255, 255, 0, 0.7)"],  # Yellow with higher opacity
                [0.8, "rgba(255, 165, 0, 0.8)"],  # Orange with more opacity
                [1.0, "rgba(255, 0, 0, 0.9)"]  # Red with full opacity
            ],
            showscale=False)

        fig.update_xaxes(range=[0, 1651],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(range=[0, 1200],
                         showgrid=False,
                         showticklabels=False,
                         #tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         domain=[0, 1])

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
                opacity=1,
                layer="below"
            )
        )

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            xaxis_title=None,
            yaxis_title=None,
            title={
                'text': f'<b>Greyscale Map Observations in {selected_city}</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            margin=dict(l=0, r=5, t=40, b=5),
            showlegend=False)
        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            title={
                'text': "<i>Please select a city to view data<i>.",
                'y': 0.6,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {
                    'size': 16,
                    'color': title_color,
                    'family': 'Arial, sans-serif'
                }},
            showlegend=False,
            margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)

        return fig

"""
-----------------------------------------------------------------------------------------
Section 10:
Definition of Box-Plot "Task Duration" (Distribution of Task Duration (A-B) per User, Color, City)
"""
@app.callback(
    Output('box_task_duration', 'figure'),
    [Input('active-button', 'data'),
     Input('city_dropdown', 'value'),
     Input('current_theme', 'data')]
)
def update_box_plot_task_duration(active_button, selected_city, current_theme):
    if active_button == 'default_viz' and selected_city is None:
        city_order = df['CityMap'].sort_values().unique().tolist()

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        fig = px.box(df,
                     x='FixationDuration_aggregated',
                     y='City',
                     # points='outliers',
                     color='description',
                     boxmode='overlay',
                     category_orders={'City': city_order},
                     color_discrete_map={
                         'color': 'blue',
                         'grey': 'lightgrey'},
                     labels={'FixationDuration_aggregated': 'Task Duration [sec.]',
                             'City': '',
                             'description': 'Map Type'})

        fig.update_traces(marker=dict(size=5), line=dict(width=2.0))

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickfont=dict(color=title_color, size=11, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(dtick=1,
                         showgrid=False,
                         showticklabels=True,
                         tickfont=dict(color=title_color, size=11, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            yaxis_title=None,
            xaxis_title={
                'text': 'Task Duration [sec.]',
                'font': {
                    'size': 11,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            title={
                'text': f'<b>Distribution of Task-Duration in sec.</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            margin=dict(l=5, r=5, t=40, b=5),
            showlegend=False)

        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title={
            'text': "<i>Please remove city selection to view overall Boxplot data.<i>",
            'y': 0.6,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 16,
                'color': title_color,
                'family': 'Arial, sans-serif'
            }},
        showlegend=False,
        margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)

    return fig

"""
-----------------------------------------------------------------------------------------
Section 11:
Definition of Box-Plot "Average Fixation Duration" (Distribution of Avg. Fixation Duration per User, Color, City)
"""
@app.callback(
    Output('box_avg_fix_duration', 'figure'),
    [Input('active-button', 'data'),
     Input('city_dropdown', 'value'),
     Input('current_theme', 'data')]
)
def update_box_plot_avg_fix_duration(active_button, selected_city, current_theme):
    if active_button == 'default_viz' and selected_city is None:
        city_order = df['CityMap'].sort_values().unique().tolist()

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        fig = px.box(df,
                     x='FixationDuration_avg',
                     y='City',
                     # points='outliers',
                     color='description',
                     boxmode='overlay',
                     category_orders={'City': city_order},
                     color_discrete_map={
                         'color': 'blue',
                         'grey': 'lightgrey'},
                     labels={'FixationDuration_aggregated': 'Average Fixation Duration [sec.]',
                             'City': '',
                             'description': 'Map Type'})

        fig.update_traces(marker=dict(size=5), line=dict(width=2.0))

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickfont=dict(color=title_color, size=11, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(dtick=1,
                         showgrid=False,
                         showticklabels=True,
                         tickfont=dict(color=title_color, size=11, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            yaxis_title=None,
            xaxis_title={
                'text': 'Average Fiation Duration [sec.]',
                'font': {
                    'size': 11,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            title={
                'text': f'<b>Distribution of average Fixation Duration in sec.</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            margin=dict(l=5, r=5, t=40, b=5),
            showlegend=False)

        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title={
            'text': "<i>Please remove city selection to view overall Boxplot data.<i>",
            'y': 0.6,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 16,
                'color': title_color,
                'family': 'Arial, sans-serif'
            }},
        showlegend=False,
        margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)

    return fig

"""
-----------------------------------------------------------------------------------------
Section 12:
Definition of Histogram (Distribution of Task Duration per selected city map)
"""
@app.callback(
    Output('hist_taskduration', 'figure'),
    [Input('city_dropdown', 'value'),
     Input('current_theme', 'data')]
)
def update_histogram_task_duration(selected_city, current_theme):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['CityMap'] == selected_city)]

        # Set title color based on theme
        title_color = 'black' if current_theme == 'light' else 'white'

        # Create histogram showing task duration per city
        fig = px.histogram(filtered_df,
                           x="FixationDuration_aggregated",
                           color="description",
                           color_discrete_map={
                               'color': 'blue',
                               'grey': 'lightgrey'},
                           #marginal="rug"
                           )

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickfont=dict(color= title_color, size=11, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_yaxes(showgrid=False,
                         showticklabels=True,
                         tickfont=dict(color=title_color, size=11, family='Arial, sans-serif'),
                         domain=[0, 1])

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper color to transparent
            yaxis_title=None,
            xaxis_title={
                'text': 'sec.',
                'font': {
                    'size': 11,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            title={
                'text': f'<b>in {selected_city}</b>',
                'font': {
                    'size': 12,
                    'family': 'Arial, sans-serif',
                    'color': title_color}
            },
            margin=dict(l=0, r=5, t=40, b=5),
            showlegend=False)
        return fig

    else:
        fig = px.scatter()

        title_color = 'black' if current_theme == 'light' else 'white'

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            title={'text': f"<i>Please select a city to view data<i>.",
                   #'y': 0.6,
                   #'x': 0.5,
                   'xanchor': 'left',
                   'yanchor': 'top',
                   'font': dict(
                       size=12,
                       color=title_color,
                       family='Arial, sans-serif')},
            showlegend=False,
            margin=dict(l=0, r=5, t=40, b=5))

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
