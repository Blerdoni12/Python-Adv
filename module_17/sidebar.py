import streamlit as st

st.sidebar_header("this is a sidebar")

st.sidebar_write("This is")

st.sidebar.selectbox("choose an option",["option 1","option 2","option 3"])
st.sidebar.radio("go to",["Home","Data","Settings"])