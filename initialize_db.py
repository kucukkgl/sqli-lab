import sqlite3, uuid

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Users table
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)""")

# Seed users only if empty
c.execute("SELECT COUNT(*) FROM users")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO users VALUES (1, 'admin', 'supersecret')")
    c.execute("INSERT INTO users VALUES (2, 'alice', 'password123')")

# Flags table
c.execute("""CREATE TABLE IF NOT EXISTS flags (
    id INTEGER PRIMARY KEY,
    flag TEXT
)""")

c.execute("SELECT COUNT(*) FROM flags")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO flags VALUES (1, 'FLAG{sql_injection_success}')")

# Sessions table
c.execute("""CREATE TABLE IF NOT EXISTS sessions (
    uuid TEXT PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)""")

# Seed sessions only if empty
c.execute("SELECT COUNT(*) FROM sessions")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO sessions VALUES (?, ?)", (str(uuid.uuid4()), 1))  # admin
    c.execute("INSERT INTO sessions VALUES (?, ?)", (str(uuid.uuid4()), 2))  # alice

conn.commit()
conn.close()
