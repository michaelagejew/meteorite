import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
df = pd.read_csv('/content/Meteorite_Landings.csv')
alt.data_transformers.disable_max_rows()
df
url = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-continents.json"
source = alt.topo_feature(url, "continent")

ch_country = alt.Chart(source).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    "equirectangular"
).properties(
    width=800,
    height=500
)

points = alt.Chart(df).mark_circle().encode(
    longitude='reclong:Q',
    latitude='reclat:Q',
    size=alt.value(10),
    tooltip='name',
    color=alt.value('slateblue')
)
ch_country + points