from dash import Dash, dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import glob
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

data_path = '../assets/all_fixation_data_cleaned_up_2.csv'
df = pd.read_csv(data_path, sep=';')
task_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].sum().reset_index()
task_duration['FixationDuration'] = task_duration['FixationDuration'] / 1000
df = pd.merge(df, task_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_aggregated'))

# Create a boxplot of the Average Task Duration per CityMap:
fig_1 = px.box(df[df['description'] == 'color'],
             x='City',
             y='FixationDuration_aggregated',
             color_discrete_sequence=['blue'],
             title='Boxplot of Average Task Duration Color')

fig_1.show()

fig_2 = px.box(df[df['description'] == 'grey'],
             x='City',
             y='FixationDuration_aggregated',
             color_discrete_sequence=['black'],
             title='Boxplot of Average Task Duration Greyscale')

fig_2.show()