# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


# First some MPG Data Exploration
@st.experimental_memo
def load_data(path):
    df = pd.read_csv(path)
    return df


dog_df_raw = load_data(path="data/processed/Dog_data.csv")
dog_df = deepcopy(dog_df_raw)

# Add title and header
st.title("Dogs in Zurich")
st.header("Zurich dog data exploration")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=dog_df)
    # st.table(data=mpg_df)

# Setting up columns
left_column, right_column = st.columns([3, 3])

# Widgets: selectbox
dog_races = ["All"]+sorted(pd.unique(dog_df['Race1']))
dog_race = left_column.selectbox("Choose Dog Race", dog_races)

# Widgets: radio buttons
show_dog_sex = right_column.radio(
    label='Choose Dog Sex', options=['All','Male', 'Female'])


# Flow control and plotting
if dog_race == "All":
    reduced_df1 = dog_df
else:
    reduced_df1 = dog_df[dog_df["Race1"] == dog_race]
sex_dict = {'Male':'m','Female':'w'}
if show_dog_sex == 'All':
    reduced_df2 = reduced_df1
else:
    reduced_df2 = reduced_df1[reduced_df1["Dog_sex"]==sex_dict[show_dog_sex]]

# In Plotly
p_fig = px.scatter(reduced_df2, x='Owner_Age_Group', y='Dog_Age', opacity=0.5,
                   range_x=[1, 9], range_y=[0, 20],
                   width=750, height=600,
                   labels={"Age": "Owner's Age",
                           "Dog_Age": "Dog Age"},
                   title="Dog Owner's Age vs. Dog Age")
p_fig.update_layout(title_font_size=22)
st.plotly_chart(p_fig)

# We can write stuff
url = "https://data.stadt-zuerich.ch/"
st.write("Data Source:", url)
# "This works too:", url

st.subheader("Streamlit Map")
ds_geo = px.data.carshare()
ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']
st.map(ds_geo)

# Sample Choropleth mapbox using Plotly GO
st.subheader("Plotly Map")

with open("data/processed/georef-switzerland-kanton.geojson") as json_file:
    cantons = json.load(json_file)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

plotly_map = go.Figure(go.Choroplethmapbox(geojson=cantons,
                                           locations=df.fips,
                                           z=df.unemp,
                                           colorscale="Viridis",
                                           zmin=0, zmax=12,
                                           marker={"opacity": 0.5, "line_width": 0}))
plotly_map.update_layout(mapbox_style="carto-positron",
                         mapbox_zoom=3,
                         mapbox_center={"lat": 37.0902, "lon": -95.7129},
                         margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(plotly_map)

