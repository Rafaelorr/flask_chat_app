import sqlite3

conn:sqlite3.Connection = sqlite3.connect('dev.db')

cursor:sqlite3.Cursor = conn.cursor()

cursor.execute('CREATE TABLE gebruikers (id INTEGER AUTO INCREMENT PRIMARY KEY, naam TEXT, wachtwoord TEXT)')
cursor.execute('CREATE TABLE emails (id INTEGER AUTO INCREMENT PRIMARY KEY, email TEXT)')
conn.commit()

conn.close()