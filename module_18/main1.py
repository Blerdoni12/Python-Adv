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

col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Books",total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating",f"{average_rating:.2f}")
col4.metric("Average Price",f"${average_price:.2f}")

st.subheader("Dataset Preview")
st.write(books_df.head())

col1,col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Book Titles")
    top_titles = books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 Authors")
    top_authors = books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

st.subheader("Genre Distribution")

fig = px.pie(
    books_df,
    names="Genre",
    title="Most Liked Genre (2009-2022)",
    color='Genre',
    color_discrete_sequence=px.colors.sequential.Plasma
)

st.plotly_chart(fig)

st.subheader("Number of Fiction vs Non Fiction Books over the years")

size = books_df.groupby(['Year', 'Genre']).size().reset_index(name='Counts')

fig = px.bar(
    size,
    x='Year',
    y='Counts',
    color='Genre',
    title="Number of Fiction vs Non Fiction Books 2009-2022",
    color_discrete_sequence=px.colors.sequential.Plasma,
    barmode='group'
)

st.plotly_chart(fig)

st.subheader("Top 15 Authors by Counts of Books Published (2009-2022)")
top_authors = books_df['Author'].value_counts().head(15).reset_index()
top_authors.columns = ['Author', 'Count']

fig = px.bar(top_authors, x='Count', y='Author', orientation='h', title='Top 15 Authors by Counts of Books Published',
             labels= {'Count': 'Counts of Books Published', 'Author': 'Author' }, color='Count',
             color_continuous_scale= px.colors.sequential.Plasma)

st.plotly_chart(fig)

st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre", books_df['Genre'].unique())
filtered_df = books_df[books_df['Genre'] == genre_filter]

st.write(filtered_df)
