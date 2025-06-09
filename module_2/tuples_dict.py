grades={
    ("John","Physics"):5,
    ("Alice","Biology"):1,
    ("Bob","English"):4,
    ("Amari","French"):3,
    ("Enesi","Chemistry"):2,
    ("Jane","Math"):5,
}

John_math = grades[('John','Physics')]
print("John's grade in math is",John_math)
grades[("Bob","English")]=3
print(grades)

keys=list(grades.keys())
student, subject = keys[0]
print(student,"'s grade in",subject,"is",John_math)