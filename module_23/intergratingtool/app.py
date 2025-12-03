import streamlit as st
import requests
import pandas as pd
from streamlit import text_input

from lesson22.api_development.clint import response

st.title('Project Management App')

st.header("Add a Developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input("Experience (Years)", min_value=0, max_value=50, value=0)

if st.button("Create Developer"):
    dev_data = {'name': dev_name, 'experience': dev_experience}
    response = requests.post(url="http://localhost:8000/developers/", json=dev_data)
    st.json(response.json())

st.header("Add a Project")
proj_title = st.text_input("Project Title")
proj_desc = st.text_area("Project Description")
proj_langs = st.text_input("Languages Used (Comma-separated)")
lead_dev_name = st.text_input("Lead Developer Name")
lead_dev_exp = st.number_input(
    "Lead Developer Experience (Years)",
    min_value=0,
    max_value=50,
    value=0
)
