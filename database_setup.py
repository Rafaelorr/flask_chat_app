import sqlite3

conn = sqlite3.connect('database.db')
print('Connected to database succesfully')

cursor = conn.cursor()
cursor.execute('INSERT INTO gebruikers VALUES (1,"test_1","test_1"),(2,"test_2","test_2")')

print('sql code succesful')
cursor.close()
conn.close()