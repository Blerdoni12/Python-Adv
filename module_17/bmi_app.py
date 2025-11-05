import streamlit as st
from abc import ABC, abstractmethod

# ========================
# Abstract Base Class
# ========================

class Person(ABC):
    """
    Abstract base class representing a person.
    """

    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self._weight = weight
        self._height = height

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value < 0:
            raise ValueError("Weight cannot be negative")
        self._weight = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value < 0:
            raise ValueError("Height cannot be negative")
        self._height = value

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    def get_info(self):
        """
        Returns person's BMI info as a dictionary.
        """
        return {
            "Name": self.name,
            "Age": self.age,
            "Weight (kg)": self.weight,
            "Height (m)": self.height,
            "BMI": round(self.calculate_bmi(), 2),
            "Category": self.get_bmi_category()
        }


# ========================
# Subclasses


class Adult(Person):
    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 24.9 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"


class Child(Person):
    def calculate_bmi(self):
        return (self.weight / (self.height ** 2)) * 1.3

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 14:
            return "Underweight"
        elif 14 <= bmi < 18:
            return "Normal weight"
        elif 18 <= bmi < 24:
            return "Overweight"
        else:
            return "Obese"


# ========================
# Streamlit BMI App
# ========================

class BMIApp:
    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def run(self):
        st.title(" BMI Calculator App")

        st.sidebar.header("Enter Personal Information")
        name = st.sidebar.text_input("Name")
        age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
        weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, step=0.1)
        height = st.sidebar.number_input("Height (m)", min_value=0.0, step=0.01)

        if st.sidebar.button("Calculate BMI"):
            if not name or height <= 0 or weight <= 0:
                st.error("⚠ Please fill out all fields with valid data.")
            else:
                if age >= 18:
                    person = Adult(name, age, weight, height)
                else:
                    person = Child(name, age, weight, height)

                self.add_person(person)
                st.success(f" Added {name}'s BMI record!")

        if self.people:
            st.subheader(" Results")
            for person in self.people:
                info = person.get_info()
                st.markdown(
                    f"**{info['Name']}**, Age: {info['Age']}<br>"
                    f"Weight: {info['Weight (kg)']} kg, Height: {info['Height (m)']} m<br>"
                    f"**BMI:** {info['BMI']} — *{info['Category']}*",
                    unsafe_allow_html=True
                )

            # Option to clear all results
            if st.button("Clear All Records"):
                self.people.clear()
                st.warning("All records cleared.")


# ========================
# Run Streamlit App
# ========================
if __name__ == "__main__":
    app = BMIApp()
    app.run()
