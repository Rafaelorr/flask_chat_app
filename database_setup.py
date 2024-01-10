import sqlite3

conn = sqlite3.connect('database.db')
print('Connected to database succesfully')

conn.execute('INSERT INTO gebruikers VALUES (1,"test","test")')

print('sql code succesful')
conn.close()