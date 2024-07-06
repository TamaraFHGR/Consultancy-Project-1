import pandas as pd
import plotly.express as px

# Data reading:
data_path = 'assets/all_fixation_data_cleaned_up_2.csv'
df = pd.read_csv(data_path, sep=';')

# Data exploration "City":
city = df['City'].unique()
map = df['CityMap'].unique()
print(city)    # 24 distinct City Maps
print(map)    # 48 distinct City Maps
px.histogram(df, x=sorted(df['City']), title='Number of fixations per city').show()

# Data exploration "User":
user = df['user'].unique()
#print(user)    # 40 distinct Users
px.histogram(df, x=sorted(df['user']), title='Number of fixations per user').show()

# Count User per City:
user_per_city = df.groupby('City')['user'].nunique()
print(user_per_city)    #