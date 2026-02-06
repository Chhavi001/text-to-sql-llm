import sqlite3

##connect to sqlite 
connection=sqlite3.connect('student.db')

##create a cursor onject to insert,record.create table,retrieve
cursor=connection.cursor()

## create the table
table_info="""
CREATE TABLE IF NOT EXISTS STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
"""
cursor.execute(table_info)

##insert some more resords
cursor.execute('''insert into STUDENT values('CHHAVI','data science','A',90)''')
cursor.execute('''insert into STUDENT values('Prateek','data science','B',100)''')
cursor.execute('''insert into STUDENT values('bushra','DEVOPS','A',86)''')
cursor.execute('''insert into STUDENT values('Aarsh','DEVOPS','A',35)''')

## display all the records
print("the inserted records are:")
data=cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

## close the connection

connection.commit()
connection.close()
