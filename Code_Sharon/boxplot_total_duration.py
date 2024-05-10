# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:39:21 2024

@author: sha_r
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data reading:
data_path = 'C:/Users/sha_r/OneDrive/Dokumente/GitHub/Consultancy-Project-1/assets/all_fixation_data_cleaned_up_2.csv'
df = pd.read_csv(data_path, sep=';')
# Task Duration in sec per User and Stimulus:
task_duration = df.groupby(['user', 'CityMap', 'description'])['FixationDuration'].sum().reset_index()
task_duration['FixationDuration'] = task_duration['FixationDuration'] / 1000
df = pd.merge(df, task_duration, on=['user', 'CityMap', 'description'], suffixes=('', '_aggregated'))
#print(df)

# -----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Annahme: Du hast bereits df und task_duration aus deinem Dashboard-Code

# Summe der Dauer pro Person pro Stadt und Ausprägung (color oder grey)
sum_duration_per_person = df.groupby(['City', 'user', 'description'])['FixationDuration'].sum().reset_index()

# Aufteilen der Daten nach description (color oder grey)
color_data = sum_duration_per_person[sum_duration_per_person['description'] == 'color']
grey_data = sum_duration_per_person[sum_duration_per_person['description'] == 'grey']

# Erstellen der Boxplots
plt.figure(figsize=(12, 8))

# Boxplot für color
sns.boxplot(data=color_data, x='City', y='FixationDuration', color='skyblue', width=0.4, linewidth=1.5, flierprops=dict(marker='o', markersize=5))

# Boxplot für grey
sns.boxplot(data=grey_data, x='City', y='FixationDuration', color='lightgrey', width=0.4, linewidth=1.5, flierprops=dict(marker='o', markersize=5))

# Ändere die Transparenz der Boxen
for patch in plt.gca().artists:
    patch.set_alpha(0.5)

# Erstelle Legende
legend_elements = [
    plt.Line2D([0], [0], color='skyblue', lw=4, label='Color'),
    plt.Line2D([0], [0], color='lightgrey', lw=4, label='Grey')
]
plt.legend(handles=legend_elements)

plt.title('Boxplot der Dauer pro Person pro Stadt (Color vs Grey)')
plt.xlabel('Stadt')
plt.ylabel('Summe der Fixationsdauer (ms)')
plt.xticks(rotation=45)
plt.grid(True)

# Automatische Anpassung der Achsenlimits
plt.tight_layout()
plt.show()
