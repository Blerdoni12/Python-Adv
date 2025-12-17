import sqlite3

conn=sqlite3.connect('example.db')
cursor=conn.cursor()

cursor.execute(
    '''
       create table if not exists students(
       student_id integer primary key,
       name text
       )
    '''
)

cursor.execute('''
    create table if not exists courses(
        course_id integer primary key,
        course_name text,
        student_id integer,
        foreign key(student_id) references students(student_id)
    )
''')

cursor.execute("insert into  students (name) values ('Alice')")
cursor.execute("insert into  students (name) values ('Amar')")

cursor.execute("insert into courses (course_name, student_id) values ('Math',1)")
cursor.execute("insert into courses (course_name, student_id) values ('Science',1)")
cursor.execute("insert into courses (course_name, student_id) values ('Art',1)")

conn.commit()

cursor.execute('''
    select students.name, courses.course_name from students join courses on students.student_id=courses.student_id
''')
rows=cursor.fetchall()
for row in rows:
    print(f"Student:{row[0]},Course:{row[1]}")