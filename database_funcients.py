import sqlite3

def connect_to_database():
  conn = sqlite3.connect('database.db')
  return conn

def close_connection(conn):
  conn.close()

def check_wachtwoord(conn,naam:str,wachtwoord:str) -> bool:
  # zoek de database voor het wachtwoord van de naam
  # als wachtwoord = opgeschozenten dan return True
  pass

def voeg_gebruikers_toe(conn,naam:str,wachtwoord:str) -> bool:
  # voeg naam en wachtwoord toe aan database
  pass
