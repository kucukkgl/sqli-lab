import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Users table
c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
c.execute("INSERT INTO users VALUES (1, 'admin', 'supersecret')")
c.execute("INSERT INTO users VALUES (2, 'alice', 'password123')")

# Flag table
c.execute("CREATE TABLE flags (id INTEGER PRIMARY KEY, flag TEXT)")
c.execute("INSERT INTO flags VALUES (1, 'FLAG{sql_injection_success}')")

conn.commit()
conn.close()
