from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
from helpers import get_flag
import base64

app = Flask(__name__)
app.secret_key = 'godofpasswordseasytoguess'

DB_NAME = 'database.db'

# -------------------- DATABASE FUNCTIONS --------------------

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('CREATE TABLE users (username TEXT, password TEXT)')
        c.execute('INSERT INTO users VALUES (?, ?)', ('admin', 'supersecret'))
        conn.commit()
        conn.close()

# -------------------- ROUTES --------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 👇 No blacklist, no sanitization — wide open!
        query = f"""
            SELECT * FROM users
            WHERE username = '{username}' AND password = '{password}'
        """

        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute(query)
            user = c.fetchone()
            conn.close()

            if user:
                session['username'] = user[0]  # username from DB
                return redirect('/dashboard')
            else:
                error = "Invalid credentials."
        except Exception as e:
            error = f"SQL Error: {e}"

    return render_template("index.html", error=error)

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))

    
    key = "recover-8491"

    users = [
        {"email": "alice@example.com", "joined": "2023-10-01"},
        {"email": "bob@example.com", "joined": "2023-11-15"},
        {"email": "charlie@example.com", "joined": "2024-01-12"}
    ]
    return render_template('dashboard.html', username=username, key=key, users=users)

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    flag = None
    error = None
    if request.method == 'POST':
        entered_key = request.form.get('key')
        if entered_key == "recover-8491":
            flag = "flag{classic_sqli_ftw}"
        else:
            error = "❌ Invalid key. Try again!"

    return render_template('unlock.html', flag=flag, error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# -------------------- APP INIT --------------------

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



