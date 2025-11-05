import streamlit as st

col1,col2,col3,col4,col5 = st.columns(5, gap="small",vertical_alignment="center")

with col1:
    st.header("Column 1")
    st.write("Conetent of column")

with col2:
    st.header("Column 2")
    st.write("Conetent of column")

with col3:
    st.header("Column 3")
    st.write("Conetent of column")

with col4:
    st.header("Column 4")
    st.write("Conetent of column")

with col5:
    st.header("Column 5")
    st.write("Conetent of column")

