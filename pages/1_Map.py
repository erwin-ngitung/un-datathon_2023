import pandas as pd
import streamlit as st
from utils import geospatial as gs

st1, st2, st3, st4, st5, st6, st7 = st.columns(7)

with st1:
    st1.image('images/un-datathon.png')

st.markdown('<h3> CO2 Emission Based on Fossil Fuel and Renewable Energy Consumption </h3>',
            unsafe_allow_html=True)

df_europe = pd.read_excel('dataset/list_europe.xlsx')
dfs = pd.read_excel('dataset/final_dataset.xlsx')
df_final = dfs[dfs['country'].isin(df_europe['country'])]
col_data = ['country', 'year', 'oil_quantity', 'renew_quantity', 'co2_value']

country = df_final['country'].unique()
year = df_final['year'].unique()
fossil = df_final['commodity_transaction_x'].unique()
renew = df_final['commodity_transaction_y'].unique()

df_map = df_final[col_data].groupby(by=['country', 'year']).sum()
df_map_final = gs.transform_data(df_map, df_final)

st8, st9 = st.columns(2)
with st8:
    add_commodity = st8.selectbox('Select the commodity:',
                                  ['oil_quantity', 'renew_quantity'])
with st9:
    add_year = st9.selectbox('Select the year:',
                            year)

st10, st11 = st.columns(2)
with st10:
    fig1 = gs.get_plotly_map(df_map_final,
                             df_final,
                             add_commodity,
                             'Distribution ' + ''.join(add_commodity.replace('_', ' ')).title())
    st10.plotly_chart(fig1,
                      theme='streamlit',
                      use_container_width=True)

with st11:
    fig2 = gs.get_plotly_map(df_map_final,
                             df_final,
                             'co2_value',
                             'Distribution CO2 Level')
    st11.plotly_chart(fig2,
                      theme='streamlit',
                      use_container_width=True)
