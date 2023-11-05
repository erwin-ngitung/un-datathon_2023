import pandas as pd
import streamlit as st
import plotly.express as px
from utils import transformation as ts

st1, st2, st3, st4, st5, st6, st7 = st.columns(7)

with st1:
    try:
        st1.image('images/un-datathon.png')
    except Exception as e:
        st1.image('../images/un-datathon.png')

st.markdown('<h3> Forecasting CO2 Emission in 2 Years </h3>',
            unsafe_allow_html=True)

try:
    df_europe = pd.read_excel('dataset/list_europe.xlsx')
    dfs = pd.read_excel('dataset/final_dataset.xlsx')
except Exception as e:
    df_europe = pd.read_excel('../dataset/list_europe.xlsx')
    dfs = pd.read_excel('../dataset/final_dataset.xlsx')

df_final = dfs[dfs['country'].isin(df_europe['country'])]
col_data = ['country', 'year', 'oil_consumption', 'renewable_production', 'CO2_emission']

country_list = df_final['country'].unique()
fossil_list = df_final['commodity_transaction_x'].unique()
renew_list = df_final['commodity_transaction_y'].unique()

df1 = df_final[col_data].groupby(by=['country', 'year']).sum()

country= st.selectbox('Select the country:',
                      country_list)
df2 = ts.transpose_data(df1)

fig = px.line(df2[df2['country'] == country],
              x='year', y='value',
              color='commodity',
              markers=True)

st.plotly_chart(fig,
                theme='streamlit',
                use_container_width=True)
