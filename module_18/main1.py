import streamlit as st
import pandas as pd
import plotly.express as px

books_df = pd.read_csv('bestsellers_with_categories.csv')

st.title("Best selling books Analysis")
st.write("This is an app for showing datasets")

st.subheader("Summery Statustics")
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()
