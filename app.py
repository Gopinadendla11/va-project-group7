import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from vega_datasets import data

df_1br_city = pd.read_csv('Datasets\City\oneBedRoom_City.csv')
df_2br_city = pd.read_csv('Datasets\City\TwoBedRoom_City.csv')
df_3br_city = pd.read_csv('Datasets\City\ThreeBedRoom_City.csv')
df_4br_city = pd.read_csv('Datasets\City\FourBedRoom_City.csv')
df_5br_city = pd.read_csv('Datasets\City\FivePlusBedRoom_City.csv')
df_single_home_city = pd.read_csv('Datasets\City\singleFamily_City.csv')
df_all_homes_city = pd.read_csv('Datasets\City\AllHomes_City.csv')

df = df_all_homes_city

selected_home_type = st.selectbox('Select Home Type',('All Homes','Single Family Homes','One Bed Room Homes','Two Bed Room Homes',
                                    'Three Bed Room Homes','Four Bed Room Homes','Five Plus Bed Room Homes'))


match selected_home_type:
    case 'Single Family Homes':
        df = df_single_home_city
    case 'One Bed Room Homes':
        df = df_1br_city
    case 'Two Bed Room Homes':
        df = df_2br_city
    case 'Three Bed Room Homes':
        df = df_3br_city
    case 'Four Bed Room Homes':
        df = df_4br_city
    case 'Five Plus Bed Room Homes':
        df = df_5br_city

df2 = df.drop(['RegionID', 'SizeRank', 'RegionType','StateName'], axis = 1)
df2 = df2.set_index('RegionName')


cities_list = df['RegionName'].tolist()
cities_list.remove("United States")

city_list = []
for term in cities_list[1:]:    
    city_list.append(term.split(', '))
    
city_state_dict = dict(city_list)
cities_list = list(city_state_dict.keys())
states_list = list(set(city_state_dict.values()))

# Creating a city list based on a state chosen
def get_city_list(state):
    spec_city_list = []
    for element in city_state_dict:
        if city_state_dict[element] == state:
            spec_city_list.append(element)
            
    return spec_city_list

col1,col2= st.columns(2)
selected_state = col1.selectbox('Select State:', states_list)
list_cities = get_city_list(selected_state)
selected_city = col2.multiselect('Select City:',list_cities,list_cities[:2])

df2 = df2.transpose()
df2.reset_index(inplace = True)
df2.rename(columns = {'index': 'Date'}, inplace = True)

# st.write(df2)


city_data =  [(city + ', ' + selected_state) for city in selected_city]
line_chart = alt.Chart(df2).mark_line().transform_fold(city_data).encode(x='Date:T',
    y=alt.Y('value:Q', title = 'Sales Prices'),
    color='key:N').properties(
    title = 'Median Sales Prices of Houses',
    width=700,
    height=500
).interactive()
st.write(' ')
st.write(line_chart)

# df_state_sale_prices = pd.read_csv('Datasets\States\sale_prices_state.csv')
# st.write(df_state_sale_prices)

# states = alt.topo_feature(data.us_10m.url, feature='states')

# alt.Chart(states).mark_geoshape().encode(
#     color='rate:Q'
# ).transform_lookup(
#     lookup='id',
#     from_=alt.LookupData(df_state_sale_prices, 'id', ['rate'])
# ).project(
#     type='albersUsa'
# ).properties(
#     width=500,
#     height=300
# )

airports = data.airports.url
states = alt.topo_feature(data.us_10m.url, feature='states')

df_test = pd.read_csv(airports,delimiter='\t')
st.write(df_test)

