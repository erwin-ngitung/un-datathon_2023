import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import pycountry as pc
from utils import geospatial as gs
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from streamlit_folium import st_folium

st1, st2, st3, st4, st5, st6, st7 = st.columns(7)

with st1:
    st1.image('images/un-datathon.png')

st.markdown('<h3> Overview greenhouse gases based on fossil fuel and renewable energy production data </h3>',
            unsafe_allow_html=True)

# # Compiling data
# df_data = pd.read_excel('dataset/dataset.xlsx')
# df_shp = gpd.read_file('dataset/world_countries/World_Countries.shp').rename(columns={'COUNTRY': 'country'})
# gs.merge_data(df_data, df_shp).to_excel('dataset/final_dataset.xlsx')

df_final = pd.read_excel('dataset/final_dataset.xlsx')
col_data = ['country', 'year', 'oil_quantity', 'renew_quantity', 'co2_value']

country = df_final['country'].unique()
year = df_final['year'].unique()
fossil = df_final['commodity_transaction_x'].unique()
renew = df_final['commodity_transaction_y'].unique()

with st.sidebar:
    add_commodity = st.selectbox('Select the commodity:',
                                 ['oil_quantity', 'renew_quantity'])
    add_year = st.selectbox('Select the year:',
                            year)

df_map = df_final[col_data].groupby(by=['country', 'year']).sum()
df_map_final = gs.transform_data(df_map, df_final)
# maps = gs.get_folium_map(df_map_final[df_map_final['year'] == add_year],
#                          'co2_value')
# st_data = st_folium(maps, height=320, width=320)

# st8, st9 = st.columns(2)
#
# with st8:
#     fig1 = px.choropleth(df_map_final,
#                          locations='iso_alpha',
#                          color=add_commodity, # lifeExp is a column of gapminder
#                          hover_name='country', # column to add to hover information
#                          color_continuous_scale=px.colors.sequential.Plasma)
#     st8.plotly_chart(fig1,
#                      theme='streamlit',
#                      use_container_width=True)
#
# with st9:
#     fig2 = px.choropleth(df_map_final,
#                          locations='iso_alpha',
#                          color='co2_value',  # lifeExp is a column of gapminder
#                          hover_name='country',  # column to add to hover information
#                          color_continuous_scale=px.colors.sequential.Plasma)
#     st9.plotly_chart(fig2,
#                      theme='streamlit',
#                      use_container_width=True)

fig = gs.get_plotly_map(df_map_final,
                        df_final,
                        add_commodity,
                        'Distribution ' + ''.join(add_commodity.replace('_', ' ')).title())
st.plotly_chart(fig,
                theme='streamlit',
                use_container_width=True)
