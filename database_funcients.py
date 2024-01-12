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
  database_wachtwoord = cur.execute(f"SELECT wachtwoord FROM gebruikers WHERE name='{naam}'")
  if database_wachtwoord == wachtwoord:
    return True
  return False

def voeg_gebruikers_toe(conn,naam:str,wachtwoord:str):
  # voeg naam en wachtwoord toe aan database
  conn.execute('')
  return
