import sqlite3

def connect_to_database():
  conn:sqlite3.Connection = sqlite3.connect('database.db')
  return conn

def close_connection(conn:sqlite3.Connection) -> None:
  conn.close()

def query_to_wachtwooord(results:list) -> str:
  results = results[0]
  results = results[1]
  results = str(results)
  return results

def voeg_email_toe(con:sqlite3.Cursor,email:str):
  cur:sqlite3.Cursor = con.cursor()
  data:tuple = (email)
  cur.execute("INSERT INTO emails (email) VALUES (?)", data)
  con.commit()

def voeg_gebruikers_toe(con:sqlite3.Connection,naam:str,wachtwoord:str) -> None:
  # voeg naam en wachtwoord toe aan database
  cursor:sqlite3.Cursor = con.cursor()
  data:tuple = (naam,wachtwoord)
  cursor.execute("INSERT INTO gebruikers (naam,wachtwoord) VALUES (?,?)", data)
  con.commit()
