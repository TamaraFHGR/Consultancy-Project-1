from dash import dash_table
from import_00_data_loader import load_and_process_data

data_path = '../assets/all_fixation_data_cleaned_up_2.csv'
df = load_and_process_data(data_path)

def update_table_container(selected_city):
    if selected_city:
        # Filter data based on the selected city
        filtered_df = df[(df['CityMap'] == selected_city)]

        # 1. Average Task Duration (seconds):
        # Sum of FixationDuration per Color / Number of Users per Color
        avg_task_color = (filtered_df[filtered_df['description'] == 'color']['FixationDuration'].sum() /
                          filtered_df[filtered_df['description'] == 'color']['user'].nunique()) / 1000
        avg_task_grey = (filtered_df[filtered_df['description'] == 'grey']['FixationDuration'].sum() /
                         filtered_df[filtered_df['description'] == 'grey']['user'].nunique()) / 1000

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
                {"KPI": "Average Task Duration", "color": f"{round(avg_task_color, 2)} sec",
                 "greyscale": f"{round(avg_task_grey, 2)} sec"},
                {"KPI": "Number of Fixation-Points", "color": fixation_points_color, "greyscale": fixation_points_grey},
                {"KPI": "Average Saccade Length", "color": round(avg_saccade_color, 2),
                 "greyscale": round(avg_saccade_grey, 2)}
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