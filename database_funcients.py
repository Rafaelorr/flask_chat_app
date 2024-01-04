import sqlite3

def connect_to_database():
  conn = sqlite3.connect('database.db')
  return conn

def close_connection(conn):
  conn.close()
