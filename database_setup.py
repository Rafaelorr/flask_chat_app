import sqlite3

conn = sqlite3.connect('database.db')
print('Connected to database succesfully')

conn.execute('CREATE TABLE gebruikers (id INTEGER PRIMARY KEY AUTOINCREMENT, naam text, wachtwoord text)')

print('sql code succesful')
conn.close()