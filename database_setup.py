import sqlite3

conn = sqlite3.connect('dev.db')

cursor = conn.cursor()

cursor.execute('IF EXIST NOT CREATE TABLE gebruikers VALUES(id INTEGER AUTO INCREMENT PRIMARY KEY, naam TEXT, wachtwoord TEXT)')

conn.close()