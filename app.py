import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, session
# from flask_session import Session

app = Flask(__name__)
app.secret_key = 'secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Session(app)

DATABASE = 'database.db'


def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)

    return conn


@app.route("/")
def home():
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # POST Method
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = get_db_connection().cursor()
        cur.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cur.fetchone()

        if user:
            session["user"] = {
                "name": user[2],
                "email": user[3],
                "image": user[4],
            }
            return redirect('profile')

        return redirect('login')

    # GET Method
    return render_template('login.html', title="Login")


@app.route('/logout')
def logout():
    session["user"] = None
    return redirect('login')


@app.route('/profile')
def profile():
    return render_template('profile.html', title="Profile", user=session["user"])


@app.route('/edit-profile')
def edit_profile():
    return render_template('profile.html', title="Profile", user=session["user"])


if __name__ == '__main__':
    app.run(debug=True)
