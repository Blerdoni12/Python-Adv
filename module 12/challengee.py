import tkinter as tk
from tkinter import messagebox


class Person:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight  # in kilograms
        self.height = height  # in meters
        self.bmi = self.calculate_bmi()

    def calculate_bmi(self):
        try:
            return round(self.weight / (self.height ** 2), 2)
        except ZeroDivisionError:
            return 0

    def get_bmi_category(self):
        raise NotImplementedError("This method should be implemented by subclasses")


class Adult(Person):
    def get_bmi_category(self):
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class Child(Person):
    def get_bmi_category(self):
        if self.bmi < 14:
            return "Underweight"
        elif 14 <= self.bmi < 18:
            return "Normal weight"
        elif 18 <= self.bmi < 20:
            return "Overweight"
        else:
            return "Obese"


# GUI App
def calculate_bmi():
    try:
        name = entry_name.get()
        age = int(entry_age.get())
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if age >= 18:
            person = Adult(name, age, weight, height)
        else:
            person = Child(name, age, weight, height)

        result = (
            f"--- BMI Report for {person.name} ---\n"
            f"Age: {person.age}\n"
            f"Weight: {person.weight} kg\n"
            f"Height: {person.height} m\n"
            f"BMI: {person.bmi}\n"
            f"Category: {person.get_bmi_category()}"
        )

        text_result.config(state='normal')
        text_result.delete('1.0', tk.END)
        text_result.insert(tk.END, result)
        text_result.config(state='disabled')

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for age, weight, and height.")


window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x450")
window.resizable(False, False)


tk.Label(window, text="Name:").pack()
entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(window, text="Age:").pack()
entry_age = tk.Entry(window)
entry_age.pack()

tk.Label(window, text="Weight (kg):").pack()
entry_weight = tk.Entry(window)
entry_weight.pack()

tk.Label(window, text="Height (m):").pack()
entry_height = tk.Entry(window)
entry_height.pack()


tk.Button(window, text="Calculate BMI", command=calculate_bmi, bg="blue", fg="white").pack(pady=10)


text_result = tk.Text(window, height=10, width=45, state='disabled', bg="#f0f0f0")
text_result.pack(pady=10)


window.mainloop()
