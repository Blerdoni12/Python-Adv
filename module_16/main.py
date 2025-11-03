import streamlit as st


if st.button("Click me"):
    st.write("You clicked me!")

if st.checkbox("Check me"):
    st.write("You checked me")

 user_input = st.text_input("Enter Text","Sample Text")

 st.write(f"You entered me: {user_input}")

age = st.number_input("Enter Age", min_value=0,max_value=100)
st.write=(f"Your age is: {age}")

message = st.text_area("Enter text")
st.write=(f"Your text is {message}")

choice = st.radio("Pick me",["choice 1","choice 2","choice 3"])

st.write(f"You chose: {choice}")

if st.button("Success"):
    st.success("Operation was successful")