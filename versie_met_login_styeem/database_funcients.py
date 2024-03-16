import sqlite3

def connect_to_database() -> sqlite3.Connection:
  conn:sqlite3.Connection = sqlite3.connect('database.db')
  return conn

def close_connection(conn:sqlite3.Connection) -> None:
  conn.close()

def query_to_wachtwooord(results:list) -> str:
  results:tuple = results[0]
  results:str = results[1]
  return results

def voeg_email_toe(con:sqlite3.Connection,email:str) -> None:
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