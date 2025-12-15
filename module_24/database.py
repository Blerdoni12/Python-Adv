import sqlite3

connection = sqlite3.connect('example.db')

cursor = connection.cursor()

cursor.execute(
    '''
        create table if not exists employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT not null,
            position text not null,
            department text not null,
            salary REAL
        )
        
    '''
)

connection.commit()

cursor.execute('''

insert into employees(name,position,department,salary)values(?, ?, ?, ?)

''',('John Doe','Software Developer','IT',7000.00))
connection.commit()

cursor.execute('select * from employees')

rows=cursor.fetchall()
for row in rows:
    print(row)

cursor.execute('''
    update employees set salary = ? where id = ?
    
''',(8000.00,1))
connection.commit()
cursor.execute('select * from employees')

rows=cursor.fetchall()

for row in rows:
    print(row)

cursor.execute('''
    delete from employees where id = ?
''', (1,))

connection.commit()
cursor.execute('select * from employees')

rows=cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()