import pandas as pd
import streamlit as st
from utils import geospatial as gs

st1, st2, st3, st4, st5, st6, st7 = st.columns(7)

with st1:
    st1.image('images/un-datathon.png')

st.markdown('<h3> Forecasting CO2 Emission in 2 Years </h3>',
            unsafe_allow_html=True)

df_europe = pd.read_excel('dataset/list_europe.xlsx')
dfs = pd.read_excel('dataset/final_dataset.xlsx')
df_final = dfs[dfs['country'].isin(df_europe['country'])]
col_data = ['country', 'year', 'oil_quantity', 'renew_quantity', 'co2_value']

country = df_final['country'].unique()
year = df_final['year'].unique()
fossil = df_final['commodity_transaction_x'].unique()
renew = df_final['commodity_transaction_y'].unique()

