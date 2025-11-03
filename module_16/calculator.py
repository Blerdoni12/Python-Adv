import streamlit as st

def calculate(num1, num2, operation):
    if operation == "Mbledhje":
        result = num1 + num2
    elif operation == "Zbritje":
        result = num1 - num2
    elif operation == "Shumzim":
        result = num1 * num2
    elif operation == "Pjestim":
        try:
            result = num1 / num2
        except ZeroDivisionError:
            result = "Cannot divide by 0"
    else:
        result = "Invalid operation"
    return result


def main():
    st.title("Simple Calculator")

    num1 = st.number_input("Enter the first number:", step=1.0)
    num2 = st.number_input("Enter the second number:", step=1.0)

    operation = st.radio(
        "Select operation:",
        ["Mbledhje", "Zbritje", "Shumzim", "Pjestim"]
    )

    result = calculate(num1, num2, operation)

    st.write(f"Result of the {operation} between {num1} and {num2} is: {result}")


if __name__ == "__main__":
    main()
