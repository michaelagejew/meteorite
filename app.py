import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv('Meteorite_Landings.csv', parse_dates=['year'])

recclasses = list(df['recclass'].unique())

st.title("Exploring Meteorite Mass and Year by Recclass and Fall Type")

st.write("This is a line chart displaying the relationship between the mass and year of meteorites, grouped by their recclass and fall type. Users can filter the data by selecting one or more recclass(es) and/or a fall type ('fell' or 'found') and a range of years. ")

recclass_select = st.multiselect("Select 'Recclass(es):'", recclasses, default=['L6'])
fall_or_found = st.multiselect("Select 'Fell' or 'Found':", ['', 'Fell', 'Found'])
year_slider = st.slider("Select range of 'Years':", 1880, 2013, (1880, 2013), step=1)
mass_range = alt.selection_interval(encodings=['y'])

filtered_df = df[df['recclass'].isin(recclass_select)]
if fall_or_found:
    filtered_df = filtered_df[filtered_df['fall'].isin(fall_or_found)]

chart = alt.Chart(filtered_df).mark_line().encode(
    x=alt.X('year', axis=alt.Axis(title='Year')),
    y=alt.Y('mass (g)', scale=alt.Scale(domain=mass_range), axis=alt.Axis(title='Mass')),
    color=alt.Color('recclass', title='Recclass'),
    opacity=alt.condition(mass_range, alt.value(1), alt.value(0.2)),
    tooltip=[
        alt.Tooltip('name', title='Name'),
        alt.Tooltip('year', title='Year'),
        alt.Tooltip('mass (g)', title='Mass'),
        alt.Tooltip('recclass', title='Recclass'),
        alt.Tooltip('GeoLocation', title='GeoLocation')
    ]
).add_selection(
    mass_range
).properties(
    title=f"Mass vs Year for {', '.join(recclass_select)} ({', '.join(fall_or_found) if fall_or_found else 'All meteors'})"
).transform_filter(
    alt.FieldRangePredicate(field='year', range=year_slider)
)

st.altair_chart(chart, use_container_width=True)


df['bin'] = pd.cut(df['mass (g)'], bins=[0, 1, 5, 10, 50, 100, 500, 1000, 10000, 100000, 1000000, 1000000000])

#group the pieces together by count
df2 = df.groupby(['bin'])['bin'].count().reset_index(name="count")

# pretty colors
my_colors = [(x/10.0, x/20.0, 0.75) for x in range(len(df))]

#print horizontal bar chart (using colors above)
#df2.plot.barh(x='bin', 
 #             y='count', 
  #            stacked=True, 
   #           color=my_colors, 
    #          title='Meteorite Landings by Mass (g)', 
     #         xlabel='Number of landings recorded by NASA',
      #        ylabel='Mass of Meteorite',
       #       figsize=(12, 4))
st.title("Masses of Meteorites")
chart = alt.Chart(df2).mark_bar().encode(
 y = 'bin',
 x= 'count'
)
st.altair_chart(chart, use_container_width = True)
