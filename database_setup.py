import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

naam = 'test_2'
wachtwoord = 'test_2'

cursor.execute(f"SELECT wachtwoord FROM gebruikers WHERE naam='{naam}'")

result = cursor.fetchone()
print(result)
conn.close()