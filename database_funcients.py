import sqlite3

def connect_to_database():
  conn = sqlite3.connect('database.db')
  return conn

def close_connection(conn):
  conn.close()
  return

def check_wachtwoord(conn,naam:str,wachtwoord:str) -> bool:
  # zoek de database voor het wachtwoord van de naam
  cur = conn.cursor()
  cur.execute(f"SELECT wachtwoord FROM gebruikers WHERE naam='{naam}'")
  database_wachtwoord = cur.fetchone()
  # maak database_wachtwoord eerste item tupel
  # database_wachtwoord = str(database_wachtwoord)
  if database_wachtwoord == wachtwoord:
    return True
  return False

def voeg_gebruikers_toe(con,naam:str,wachtwoord:str) -> None:
  # voeg naam en wachtwoord toe aan database
  cursor = con.cursor()
  data = (naam,wachtwoord)
  cursor.execute("INSERT INTO gebruikers (naam,wachtwoord) VALUES (?, ?)", data)
  con.commit()
  return
