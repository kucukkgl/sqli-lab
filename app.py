from flask import Flask, request, render_template, make_response,redirect

import sqlite3
import datetime

app = Flask(__name__)

def log_query(query):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr or "unknown"
    suspicious = "⚠️" if any(x in query.lower() for x in ["--", "' or", "union", "sqlite_master", "flags"]) else ""
    log_line = f"[{timestamp}] {ip} → {query} {suspicious}\n"
    with open("app.log", "a") as f:
        f.write(log_line)

def log_error(error, query=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr or "unknown"
    log_line = f"[{timestamp}] {ip} ERROR: {error}"
    if query:
        log_line += f" | Query: {query}"
    log_line += "\n"
    with open("error.log", "a") as f:
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        log_query(query)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchone()
        except Exception as e:
            log_error(str(e), query)
            result = None
        conn.close()

        if result:
            session_id = result[0]
            resp = make_response(redirect("/profile"))
            resp.set_cookie("session_id", str(session_id))
            return resp
        else:
            return render_template("login.html", error="Login failed. Try again.")

    return render_template("login.html")

@app.route("/profile")
def profile():
    session_id = request.cookies.get("session_id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id=?", (session_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return render_template("profile.html", username=result[1], session_id=result[0])
    else:
        return redirect("/login")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
