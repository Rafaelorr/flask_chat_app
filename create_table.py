import sqlite3

conn = sqlite3.connect('database.db')
print('Connected to database succesfully')

conn.execute('CREATE TABLE students (name TEXT, addr TEXT)')
print('Created table successfully')
conn.close()