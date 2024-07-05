import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title('Ola Mundo')

# df = pd.read_feather('data/dados.feather')
df = st.session_state['df']

df.shape
df