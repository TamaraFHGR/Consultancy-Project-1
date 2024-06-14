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
data_path = '../assets/all_fixation_data_cleaned_up.csv'
df = pd.read_csv(data_path, sep=';')
"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""
app.layout = html.Div([
    html.Div(
        id='header-area',
        children=[
            html.H1('Dashboard for the visual analysis of Eye-Tracking data,'),
            html.H1("based on Metro Maps of different Cities.")

        ]
    ),
    html.Div(
        id='dropdown-area',
        children=[
            html.P("Please select a City-Map:"),
            dcc.Dropdown(
                id='dropdown_city',
                options=[{'label': city, 'value': city} for city in sorted(df['CityMap'].unique())]
            ),
        ]
    ),
    # Zeile 1:
    dbc.Row([
        dbc.Col(
            html.Img(
                id='city_image',
                style={'width': '90%', 'height': 'auto%'}),
            width=6),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='dropdown_user_color',
                    options=[
                        {'label': user,
                         'value': user}
                        for user in sorted(df[df['description'] == 'color']['user'].unique())],
                ),
                dcc.Graph(
                    id="scatter_plot_color"),
                html.P("Select a range of Fixation Duration"),
                dcc.RangeSlider(
                    id='range_slider_color',
                    min=df[df['description'] == 'color']['FixationDuration'].min(),
                    max=df[df['description'] == 'color']['FixationDuration'].max(),
                    step=None,
                    value=[
                        df[df['description'] == 'color']['FixationDuration'].min(),
                        df[df['description'] == 'color']['FixationDuration'].max()
                    ],
                )
            ],width=6)
    ]),
    # Zeile 2:
    dbc.Row([
        dbc.Col(
            html.Div(
                id="table_container"
            ), width=6),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='dropdown_user_grey',
                    options=[
                        {'label': user,
                         'value': user}
                        for user in sorted(df[df['description'] == 'gray']['user'].unique())],
                ),
                dcc.Graph(
                    id="scatter_plot_grey"),
                html.P("Select a range of Fixation Duration"),
                dcc.RangeSlider(
                    id='range_slider_grey',
                    min=df[df['description'] == 'gray']['FixationDuration'].min(),
                    max=df[df['description'] == 'gray']['FixationDuration'].max(),
                    step=None,
                    value=[
                        df[df['description'] == 'gray']['FixationDuration'].min(),
                        df[df['description'] == 'gray']['FixationDuration'].max()
                    ],
                )
            ],width=6)
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
    [Input('dropdown_city', 'value'),
     Input('dropdown_user_color', 'value'),
     Input('range_slider_color', 'value')]
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
            user_filter = df[
                'user'].notnull()  # If 'All' users or no user selected, include all non-null user entries
        else:
            user_filter = (df['user'] == selected_user)  # Specific user is selected

        # Filter and sort data based on the selected filters
        filtered_df = df[
            (df['CityMap'] == selected_city) &
            (df['description'] == 'color') &
            user_filter &
            (df['FixationDuration'] >= slider_value_color[0]) &
            (df['FixationDuration'] <= slider_value_color[1])
            ].sort_values(by='FixationIndex')

        # Define the maximum extents for the plot
        max_x = filtered_df['MappedFixationPointX'].max()
        min_x = filtered_df['MappedFixationPointX'].min()
        max_y = filtered_df['MappedFixationPointY'].max()
        min_y = filtered_df['MappedFixationPointY'].min()

        # Create scatter plot using the color map
        fig = px.scatter(filtered_df,
                         x='MappedFixationPointX',
                         y='MappedFixationPointY',
                         size='FixationDuration',
                         color='user',
                         color_discrete_map=color_map,
                         title=('Colored Metro Map Observations in ' + selected_city),
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
                    name=f"Path for {user}"
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
    [Input('dropdown_city', 'value'),
     Input('dropdown_user_grey', 'value'),
     Input('range_slider_grey', 'value')]
)
def update_scatter_plot_grey(selected_city, selected_user, slider_value_grey):
    if selected_city:
        # Check if a user is selected or the "All" option is chosen
        if selected_user == 'All' or not selected_user:
            user_filter = (
                df['user'].notnull())  # If 'All' users or no user selected, include all non-null user entries
        else:
            user_filter = (df['user'] == selected_user)  # Specific user is selected
        # Filter data based on the selected filters
        filtered_df = df[
            (df['City'] == selected_city) &
            (df['description'] == 'gray') &
            user_filter &
            (df['FixationDuration'] >= slider_value_grey[0]) &
            (df['FixationDuration'] <= slider_value_grey[1])
            ]
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
        fig["layout"].pop("updatemenus")  # optional, drop animation buttons
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
        )
        return fig
    else:
        return px.scatter(title='Please select a city to view data')



if __name__ == '__main__':
    app.run_server(debug=True)
