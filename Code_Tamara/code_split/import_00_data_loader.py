import pandas as pd
#data_path = 'assets/all_fixation_data_cleaned_up_2.csv'

def load_and_process_data(data_path):
    df = pd.read_csv(data_path, sep=';')

    # Task Duration in sec per User and Stimulus:
    task_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].sum().reset_index()
    task_duration['FixationDuration'] = task_duration['FixationDuration'] / 1000
    df = pd.merge(df, task_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_aggregated'))

    return df
