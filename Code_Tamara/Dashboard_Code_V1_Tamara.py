import ipywidgets as widgets
from ipywidgets import interact
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Pseudowerte für Eyetracking-Daten generieren
np.random.seed(0)
n_points = 100
x = np.random.uniform(0, 100, n_points)
y = np.random.uniform(0, 100, n_points)
duration = np.random.uniform(50, 500, n_points)
fixation_point = np.random.choice(['A', 'B', 'C', 'D'], size=n_points)
gaze_category = np.random.choice(['X', 'Y', 'Z'], size=n_points)

eyetracking_data = pd.DataFrame(
    {'X': x, 'Y': y, 'Duration': duration, 'FixationPoint': fixation_point, 'GazeCategory': gaze_category})


# Funktion zur Erstellung der Plots basierend auf den Filtern
def plot_data(filter_value_1, filter_value_2, filter_value_3, filter_value_4, filter_value_5):
    filtered_data = eyetracking_data[(eyetracking_data['X'] <= filter_value_1) &
                                     (eyetracking_data['Y'] <= filter_value_2) &
                                     (eyetracking_data['Duration'] >= filter_value_3) &
                                     (eyetracking_data['Duration'] <= filter_value_4) &
                                     (eyetracking_data['FixationPoint'] == filter_value_5)]

    if filtered_data.empty:
        print("Keine Daten gefunden!")
        return

    plt.figure(figsize=(15, 15))

    # Bild anzeigen mit Rahmen
    plt.subplot(2, 2, 1)
    plt.text(0.5, 0.5, 'Hier könnte deine Karte sein', horizontalalignment='center', verticalalignment='center',
             fontsize=15)
    plt.axis('off')
    plt.title('Karte als Bild')
    plt.gca().set_frame_on(True)
    plt.gca().spines['top'].set_linewidth(1)
    plt.gca().spines['bottom'].set_linewidth(1)
    plt.gca().spines['left'].set_linewidth(1)
    plt.gca().spines['right'].set_linewidth(1)

    # Heatmap mit Rahmen
    plt.subplot(2, 2, 2)
    sns.kdeplot(data=filtered_data, x='X', y='Y', fill=True, cmap='Blues', thresh=0, levels=100)
    plt.title('Heatmap')
    plt.gca().set_frame_on(True)
    plt.gca().spines['top'].set_linewidth(1)
    plt.gca().spines['bottom'].set_linewidth(1)
    plt.gca().spines['left'].set_linewidth(1)
    plt.gca().spines['right'].set_linewidth(1)

    # KPIs Zahlen (Durchschnittliche Duration) mit Rahmen
    plt.subplot(2, 2, 3)
    kpi_data = filtered_data['Duration'].mean()
    plt.text(0.5, 0.5, f'Durchschnittliche Duration:\n{kpi_data:.2f}', horizontalalignment='center',
             verticalalignment='center', fontsize=15)
    plt.axis('off')
    plt.title('Durchschnittliche Duration')
    plt.gca().set_frame_on(True)
    plt.gca().spines['top'].set_linewidth(1)
    plt.gca().spines['bottom'].set_linewidth(1)
    plt.gca().spines['left'].set_linewidth(1)
    plt.gca().spines['right'].set_linewidth(1)

    # Gaze Plot (Scatter Plot) mit Rahmen
    plt.subplot(2, 2, 4)
    sns.scatterplot(data=filtered_data, x='X', y='Y', hue='GazeCategory')
    plt.title('Gaze Plot')
    plt.gca().set_frame_on(True)
    plt.gca().spines['top'].set_linewidth(1)
    plt.gca().spines['bottom'].set_linewidth(1)
    plt.gca().spines['left'].set_linewidth(1)
    plt.gca().spines['right'].set_linewidth(1)

    plt.tight_layout()
    plt.show()


# Interaktive Widgets für die Filter erstellen
filter_widget_1 = widgets.FloatSlider(
    value=100,
    min=0,
    max=100,
    step=1,
    description='Filter X:',
    continuous_update=False
)

filter_widget_2 = widgets.FloatSlider(
    value=100,
    min=0,
    max=100,
    step=1,
    description='Filter Y:',
    continuous_update=False
)

filter_widget_3 = widgets.FloatSlider(
    value=50,
    min=0,
    max=500,
    step=1,
    description='Filter Min Duration:',
    continuous_update=False
)

filter_widget_4 = widgets.FloatSlider(
    value=500,
    min=0,
    max=500,
    step=1,
    description='Filter Max Duration:',
    continuous_update=False
)

filter_widget_5 = widgets.Dropdown(
    options=['A', 'B', 'C', 'D'],
    value='A',
    description='Fixation Point:',
    continuous_update=False
)

# Das Dashboard-Layout erstellen
dashboard_layout = widgets.VBox([
    widgets.HTML("<h1>Mein Eyetracking-Dashboard</h1>"),
    widgets.HBox([filter_widget_1, filter_widget_2]),
    widgets.HBox([filter_widget_3, filter_widget_4, filter_widget_5]),
    widgets.interactive_output(plot_data, {'filter_value_1': filter_widget_1,
                                           'filter_value_2': filter_widget_2,
                                           'filter_value_3': filter_widget_3,
                                           'filter_value_4': filter_widget_4,
                                           'filter_value_5': filter_widget_5})
])

# Das Dashboard anzeigen
dashboard_layout
