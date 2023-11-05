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

st.markdown('<h3> Overview of CO2 Emission based on Fossil Fuel and Renewable Energy Production Data </h3>',
            unsafe_allow_html=True)
