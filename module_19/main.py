import pandas as pd
import streamlit as st
import plotly.express as px


books_df = pd.read_csv('bestsellers_with_categories.csv')

st.title("Best Selling Books Analysis")
st.write("This app analyzes Amazon best-selling books.")



st.sidebar.header("Add New Book Data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author Name")
    new_user_rating = st.slider("User Rating", 0.0, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Reviews", min_value=0, step=1)
    new_price = st.number_input("Price", min_value=0, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2025, step=1)
    new_genre = st.selectbox("Genre", books_df['Genre'].unique())
    submit_button = st.form_submit_button(label="Add Book")

if submit_button:
    new_data = {
        "Name": new_name,
        "Author": new_author,
        "User Rating": new_user_rating,   # FIXED
        "Reviews": new_reviews,
        "Price": new_price,
        "Year": new_year,
        "Genre": new_genre,
    }

    books_df = pd.concat([pd.DataFrame([new_data]), books_df], ignore_index=True)
    books_df.to_csv('bestsellers_with_categories.csv', index=False)
    st.sidebar.success("New book added!")


st.subheader("Summary Statistics")

total_books = len(books_df)
unique_titles = books_df['Name'].nunique()        # FIXED
average_rating = books_df['User Rating'].mean()   # FIXED
average_price = books_df['Price'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"${average_price:.2f}")

st.subheader("Dataset Preview")
st.write(books_df.head())
