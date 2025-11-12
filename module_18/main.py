import streamlit as st
import pandas as pd

st.header('Display Data frame')

data = pd.DataFrame({
    'Name':['Blerdon','Amar','Obama'],
    'Age': [15,14,69],
    'City':['Drenas','Prishtina','Washington']
})
st.dataframe(data)