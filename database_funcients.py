import sqlite3

def connect_to_database():
  conn = sqlite3.connect('database.db')
  return conn

def close_connection(conn):
  conn.close()
  return

def query_to_string(results:list) -> str:
  results = results[0]
  results = results[1]
  results = str(results)

def voeg_email_toe(con,email:str):
  cur = con.cursor()
  data = (email)
  cur.execute("INSERT INTO emails (email) VALUES (?)", data)
  con.commit()
  return

def voeg_gebruikers_toe(con,naam:str,wachtwoord:str) -> None:
  # voeg naam en wachtwoord toe aan database
  cursor = con.cursor()
  data = (naam,wachtwoord)
  cursor.execute("INSERT INTO gebruikers (naam,wachtwoord) VALUES (?, ?)", data)
  con.commit()
  return
