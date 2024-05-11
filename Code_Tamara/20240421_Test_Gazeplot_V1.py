from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from PIL import Image
import numpy as np

#------------------------------------------------------------

# Data reading:
data_path = 'daten_prototyp_Antw_p1_color.csv'
df = pd.read_csv(data_path,
                 sep=';',
                 usecols=['MappedFixationPointX', 'MappedFixationPointY', 'FixationDuration', 'FixationIndex'])

# Image reading and converting to NumPy array:
img_path = '01_Antwerpen_S1_Color.jpg'
img = Image.open(img_path)
img_width, img_height = img.size
img_array = np.array(img)

# Inverting the Y-axis for proper alignment:
df['MappedFixationPointY'] = img_height - df['MappedFixationPointY']

#------------------------------------------------------------

# Create a scatter plot on top of the image:
fig = px.imshow(img_array, binary_string=True)
fig.add_scatter(x=df['MappedFixationPointX'], y=df['MappedFixationPointY'],
                mode='markers', marker=dict(size=df['FixationDuration'], opacity=0.5))

# Set the axes' properties to align with the image:
fig.update_xaxes(range=[0, img_width], showgrid=False, zeroline=False, scaleanchor="y", scaleratio=1)
fig.update_yaxes(range=[0, img_height], showgrid=False, zeroline=False)

# Update figure layout to ensure correct alignment and sizing:
fig.update_layout(
    title='Gaze Plot on Image Background',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    xaxis_fixedrange=True,
    yaxis_fixedrange=True,
    autosize=False,
    width=img_width,
    height=img_height
)

# Initialization of the Dash app:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Eye-Tracking Data Analysis"

# App Layout:
app.layout = html.Div(
    id="app-container",  # Div container for the app
    children=[
        html.H1("Eye-Tracking Gaze Plot Visualization"),
        html.P("This dashboard visualizes the gaze plot of the eye-tracking data on the image background."),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False)
