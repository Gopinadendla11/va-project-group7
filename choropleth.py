import pandas as pd
import streamlit as st
import altair as alt
import numpy as num
import re
from vega_datasets import data

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Setting up dataframe
df = pd.read_csv('Metro_mlp_uc_sfrcondo_sm_month.csv')

state_codes = [1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]
state_abv = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
temp_list = list(zip(state_abv, state_codes))
states_info = pd.DataFrame(temp_list, columns = ['StateName', 'id'])

df3 = pd.merge(df, states_info, how = 'inner', on = 'StateName')
temp = df3.pop('id')
df3.insert(5, 'id', temp)
df3 = df3.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType'], axis = 1)



date_values = list(df3[1:].columns.values)

# Creating a date list based on a year chosen
def return_date_list(year):
    date_list = []
    for date in date_values:
        if str(year) in date:
            date_list.append(date)
        
    return date_list


# --MAIN--
# Sidebar menu
with st.sidebar:
    st.header('Choropleth Map Options')
    
    # Date selections
    #year_selection = st.selectbox('Select Year:', ['2018', '2019', '2020', '2021', '2022'])
    year_selection = st.slider('Select Year:', min_value = 2018, max_value = 2022, value = 2018)
    
    if year_selection:
        year = return_date_list(year_selection)
        month_selection = st.selectbox('Select Month:', year)
        
    # Choosing Sum or Average of prices
    calculation = st.selectbox('Choose to Sum or Average state prices:', ['Sum', 'Average'])
    if calculation == 'Sum':
        df3_final = df3.groupby(['StateName', 'id'])[month_selection].sum().reset_index()
        label_text = 'Sum'
        
    if calculation == 'Average':
        df3_final = round(df3.groupby(['StateName', 'id'])[month_selection].mean(), 2).reset_index()
        label_text = 'Average'
    
    # Renaming column to make sense to users
    label = label_text + ' of Housing Prices ($)'
    df3_final.rename(columns = {month_selection: label, 'StateName': 'State Name'}, inplace = True)

    
states = alt.topo_feature(data.us_10m.url, 'states')

# Choropleth Map
st.header('Choropleth Map of Zillow Housing Prices in the US')
choropleth_map = alt.Chart(states).mark_geoshape().encode(
    color = label + ':Q',
    tooltip = ['State Name:O', label + ':Q']
).transform_lookup(
    lookup = 'id',
    from_ = alt.LookupData(df3_final, 'id', ['State Name', label])
).project(
    type = 'albersUsa'
).properties(
    width = 800,
    height = 600
)

choropleth_map