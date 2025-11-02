from flask import Flask, request, render_template, make_response
import sqlite3
import datetime

app = Flask(__name__)

def log_query(query):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr or "unknown"
    suspicious = "⚠️" if any(x in query.lower() for x in ["--", "' or", "union", "sqlite_master", "flags"]) else ""
    log_line = f"[{timestamp}] {ip} → {query} {suspicious}\n"
    with open("logs.txt", "a") as f:
        f.write(log_line)
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    user = request.args.get('user', '')
    query = f"SELECT * FROM users WHERE username = '{user}'"
    log_query(query)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result = '<br>'.join(str(row) for row in rows)
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return f"<h3>Results:</h3><p>{result}</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        log_query(query)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                resp = make_response(f"Welcome, {username}!")
                resp.set_cookie("session_id", username)
                return resp
            else:
                return "Login failed."
        except Exception as e:
            return f"Error: {e}"

@app.route('/profile')
def profile():
    session_id = request.cookies.get("session_id", "")
    query = f"SELECT * FROM users WHERE username = '{session_id}'"
    log_query(query)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result = '<br>'.join(str(row) for row in rows)
    except Exception as e:
        result = f"Error: {e}"
    conn.close()
    return f"<h3>Session Profile:</h3><p>{result}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
