import plotly.express as px
import glob
from import_00_data_loader import load_and_process_data

data_path = '../assets/all_fixation_data_cleaned_up_2.csv'
df = load_and_process_data(data_path)

def get_image_path_grey(selected_city):
    file_pattern_grey = f'assets/*_{selected_city}_Grey.jpg'
    matching_files = glob.glob(file_pattern_grey)
    if matching_files:
        return 'http://127.0.0.1:8050/' + matching_files[0]


def update_heat_map_grey(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = (df[
            (df['CityMap'] == selected_city)] & (df['description'] == 'grey'))

        # Create density contour plot
        fig = px.density_contour(filtered_df,
                                 x='MappedFixationPointX',
                                 y='MappedFixationPointY',
                                 nbinsx=20,
                                 nbinsy=20,
                                 title=('Color Map Observations in ' + selected_city),)

        fig.update_xaxes(range=[0, 1650])
        fig.update_yaxes(range=[0, 1200])

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
                sizing="contain",
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