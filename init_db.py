import sqlite3
import datetime
import time

db = sqlite3.connect('database.sqlite3')

try:
    db.execute('DROP TABLE Comments')
    db.execute('DROP TABLE Visits')
    db.execute('DROP TABLE Views')
except:
    pass
db.execute('CREATE TABLE Comments(id integer PRIMARY KEY AUTOINCREMENT, ip text, user_agent text, timestamp integer, name text, message text)')
db.execute('CREATE TABLE Visits(id integer PRIMARY KEY AUTOINCREMENT, ip text, user_agent text, timestamp integer)')
db.execute('CREATE TABLE Views(today integer, total integer, timestamp integer)')
today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
timestamp = time.mktime(today.timetuple())
db.execute('INSERT INTO Views(today, total, timestamp) VALUES (?, ?, ?)', (0, 0, timestamp))
db.execute('INSERT INTO Comments(ip, user_agent, timestamp, name, message) VALUES (?, ?, ?, ?, ?)',
    ("127.0.0.1", "google chrome", time.time(), "123", "Simple Text"))
db.commit()