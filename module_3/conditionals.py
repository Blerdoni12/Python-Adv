#example 1
age = 18

if age >=18:
    print("You can vote.")
else:
    print("You can not vote yet.")

#example 2
temperature = 28

if temperature >30:
    print("Its a hot day,stay hydrated")
elif 20<= temperature<=30:
    print("the weather is pleasent")
else:
    print("Its a cold day!")

#example 3
student_gpa=4.5
student_score=75

if student_gpa>=3.5:
    if 50<= student_score<=65:
        print(f"Student with GPA {student_gpa} and test score of {student_score} may be eligible for a partial scholarship")
    elif student_score > 65:
        print(f"Student with GPA {student_gpa} and test score of {student_score} is eligible for a full scholarship")
    else:
        print(f"Student with GPA {student_gpa} and test score of {student_score} is not eligible for a scholarship")
else:
    print(f"Student with GPA {student_gpa} and test score of {student_score} is not eligible for a scholarship")

