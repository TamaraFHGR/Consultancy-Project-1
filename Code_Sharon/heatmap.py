import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

# Daten einlesen
data_path = 'C:/Users/sha_r/OneDrive/Dokumente/GitHub/Consultancy-Project-1/assets/all_fixation_data_cleaned_up_2.csv'
df = pd.read_csv(data_path, sep=';')

# Filtern der Daten für die Stadt "Antwerpen_S1" und die Farbkarte
filtered_df = df[(df['CityMap'] == 'Antwerpen_S1') & (df['description'] == 'color')]
#----------------------------------------------------------------------


# Erstellen der Heatmap mit Plotly Express
fig = px.density_contour(filtered_df,
                         x='MappedFixationPointX',
                         y='MappedFixationPointY',
                         nbinsx=20,
                         nbinsy=20,
                         title='Color Map Observations in Antwerpen_S1')

# Anpassungen am Layout (z. B. Hintergrundbild hinzufügen)

# Plot in Spyder anzeigen
fig.show(renderer='png')

# Alternativ kannst du den Plot auch in eine Matplotlib-Figur konvertieren und anzeigen lassen
# matplot_fig = fig.to_plotly()
# plt.clf()
# plt.imshow(matplot_fig)
# plt.show()



#----------------------------------------------------------------------


# Konvertieren der Daten in eine 2D-Histogramm-Matrix
heatmap, xedges, yedges = np.histogram2d(filtered_df['MappedFixationPointX'], filtered_df['MappedFixationPointY'], bins=20)

# Plot der Heatmap mit Matplotlib
plt.imshow(heatmap.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
plt.title('Color Map Observations in Antwerpen_S1')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.colorbar(label='Density')
plt.show()
