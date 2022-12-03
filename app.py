import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data

# Data Sources
counties = alt.topo_feature(data.us_10m.url, 'counties')

df_rates = pd.read_csv('unemployment.tsv', delimiter='\t')
df_rates['rate_emp'] = 1 - df_rates['rate']

# Radio button
option = st.radio("What to you want to show?", ('rate', 'rate_emp'))

# title
if option == 'rate':
    st.write('Unemployment Rate')
else:
    st.write("Employment Rate")

# MAP
ch_map = alt.Chart(counties).mark_geoshape().encode(
    color=option+':Q',
    tooltip=['id:O', option+':Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_rates, 'id', ['rate', 'rate_emp'])
).project(
    type='albersUsa'
).properties(
    width=600,
    height=400
)

# Show 
st.write(ch_map)