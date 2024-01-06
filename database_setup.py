import sqlite3

conn = sqlite3.connect('database.db')
print('Connected to database succesfully')

conn.execute('INSERT into gebruikers (id,naam,wachtwoord) values (1,"test","test")')

print('sql code succesful')
conn.close()