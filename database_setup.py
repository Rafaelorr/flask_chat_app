import sqlite3

conn = sqlite3.connect('database.db')
print('Connected to database succesfully')

conn.close()