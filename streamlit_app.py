import pandas as pd
import streamlit as st
import altair as alt
import numpy as num
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Setting up dataframe
df = pd.read_csv('Datasets/City/Metro_invt_fs_uc_sfrcondo_sm_month.csv')

df2 = df
df2 = df2.set_index('RegionName')

df2_transposed = df2.drop(['RegionID', 'SizeRank', 'RegionType', 'StateName'], axis = 1)
df2_transposed = df2_transposed.transpose()
df2_transposed.reset_index(inplace = True)
df2_transposed.rename(columns = {'index': 'Date'}, inplace = True)

# Removing periods in column names (periods cause problems for Altair)
array = []
for columns in df2_transposed.columns:    
    new_name = re.sub(r'[.]', '', columns)        
    array.append(new_name)

df2_transposed.columns = array

col_values = df['RegionName'].tolist()
area_list = [['', 'USA']]

for term in col_values[1:]:    
    area_list.append(term.split(', '))
    
area_dict = dict(area_list)
city_list = list(area_dict.keys())
state_list = list(set(area_dict.values()))
city_list.sort()
state_list.sort()


# Creating a city list based on a state chosen
def return_city_list(state):
    spec_city_list = []
    for element in area_dict:
        if area_dict[element] == state:
            new_element = re.sub(r'[.]', '', element) 
            spec_city_list.append(new_element)
            
    return spec_city_list



# --MAIN--
# Sidebar menu
with st.sidebar:
    # First selections
    state_selection1 = st.selectbox('Select First State:', state_list)
    cities1 = return_city_list(state_selection1)
    
    if state_selection1 and state_selection1 == 'USA':
        chart_list = ['United States']
    
    elif state_selection1:
        city_selection1 = st.multiselect('Select Cities:', cities1, cities1[:2])
        
        # Getting info to display on multi-line chart
        chart_list = [(city + ', ' + state_selection1) for city in city_selection1]
        
        
    # Second selections
    state_selection2 = st.selectbox('Select Second State:', state_list, index = 1)
    cities2 = return_city_list(state_selection2)
    
    if state_selection2 and state_selection2 == 'USA':
        chart_list = ['United States']
    
    elif state_selection2:
        city_selection2 = st.multiselect('Select Cities: ', cities2, cities2[:2])
        
        # Getting info to display on multi-line chart
        chart_list = chart_list + [(city + ', ' + state_selection2) for city in city_selection2]

# Multi-Line Chart
multi_lc = alt.Chart(df2_transposed).mark_line().transform_fold(
    chart_list
).encode(
    x = 'Date:T',
    y = alt.Y('value:Q', title = 'Sales Prices ($)'),
    color = 'key:N'
).properties(
    title = 'Inventory Sales Prices of Houses',
    width = 950,
    height = 600
).interactive()

multi_lc


# Choropleth Map
