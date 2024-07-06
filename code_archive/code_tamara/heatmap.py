from dash import Dash, dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

data_path = '../assets/all_fixation_data_cleaned_up_2.csv'
df = pd.read_csv(data_path, sep=';')
# Task Duration in sec per User and Stimulus:
task_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].sum().reset_index()
task_duration['FixationDuration'] = task_duration['FixationDuration'] / 1000
df = pd.merge(df, task_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_aggregated'))

app.layout = html.Div([
    html.Div(
        id='selection-area',
        children=[
            html.P('Please select a City-Map:'),
            dcc.Dropdown(
                id='dropdown_city',
                options=[{'label': city, 'value': city} for city in sorted(df['CityMap'].unique())]
            )
        ]
    ),
    html.Div(
        id='color_plot_area',
        children=[
            # Zeile 1 - Color-Plot-Area:
            html.Img(
                id='city_image_color',
                style={'width': '90%', 'height': 'auto'}
            ),
            dcc.Graph(
                id='plot_color_2'
            ),
            html.P('Select a User'),
            dcc.Dropdown(
                id='dropdown_user_color_2',
                options=[{'label': user, 'value': user} for user in
                         sorted(df[df['description'] == 'color']['user'].unique())]
            ),
            html.P('Select a range of Task Duration'),
            dcc.RangeSlider(
                id='range_slider_color_2',
                min=1,
                max=50,
                step=None,
                value=[
                    df[df['description'] == 'color']['FixationDuration_aggregated'].min(),
                    df[df['description'] == 'color']['FixationDuration_aggregated'].max()
                ]
            )
        ]
    )
])


@app.callback(
    Output('plot_color_2', 'figure'),
    [Input('dropdown_city', 'value'),
     Input('dropdown_user_color_2', 'value'),
     Input('range_slider_color_2', 'value')]
)

def update_heatmap_color(selected_city, selected_user, slider_value_color):
    if not selected_city:
        return px.scatter()  # Leeres Plot anzeigen, wenn keine Stadt ausgewählt ist

    filtered_df = df[(df['CityMap'] == selected_city) & (df['description'] == 'color')]
    if selected_user != 'All':
        filtered_df = filtered_df[filtered_df['user'] == selected_user]

    filtered_df = filtered_df[
        (filtered_df['FixationDuration'] >= slider_value_color[0]) &
        (filtered_df['FixationDuration'] <= slider_value_color[1])
        ]

    fig = px.density_heatmap(filtered_df, x='MappedFixationPointX', y='MappedFixationPointY', nbinsx=20, nbinsy=20)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
