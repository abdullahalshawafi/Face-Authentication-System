import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, session
import skimage.io as io
import sys
sys.path.append("./cartonize") 
from cartonize import cartoonize

app = Flask(__name__)
app.secret_key = "secret key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


DATABASE = "database.db"


def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)

    print("CONNECTED SUCCESSFULLY TO DATABASE")
    return conn


@app.route("/")
def home():
    if not session["user"]:
        return redirect("login")
    return render_template("profile.html", title="Profile", user=session["user"])


@app.route("/login", methods=["GET", "POST"])
def login():
    # POST Method
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = get_db_connection().cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
        )
        user = cur.fetchone()

        if user:
            session["user"] = {
                "name": user[2],
                "email": user[3],
                "image": user[4],
            }
            return redirect("profile")

        return redirect("login")

    # GET Method
    return render_template("login.html", title="Login")


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("login")


@app.route("/profile")
def profile():
    if not session["user"]:
        return redirect("login")
    return render_template("profile.html", title="Profile", user=session["user"])


@app.route("/edit-profile")
def edit_profile():
    if not session["user"]:
        return redirect("login")
    return render_template("profile.html", title="Profile", user=session["user"])


@app.route("/cartonize", methods=["GET", "POST"])
def cartonize():
    if request.method == "POST":
        if "cartonized_" not in str(session["user"].get("image")):
            originalImage = io.imread(
                "./static/images/" + str(session["user"].get("image"))
            )
            cartonizedImage = cartoonize(originalImage)
            io.imsave(
                "./static/images/cartonized_" + str(session["user"].get("image")),
                cartonizedImage,
            )
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE users SET image = ? WHERE email = ?",
                (
                    "cartonized_" + session["user"].get("image"),
                    session["user"].get("email"),
                ),
            )
            try:
                connection.commit()
                session["user"] = {
                    "name": session["user"].get("name"),
                    "email": session["user"].get("email"),
                    "image": "cartonized_" + session["user"].get("image"),
                }
            except Error as e:
                print(e.message)
        else:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE users SET image = ? WHERE email = ?",
                (
                    session["user"].get("image").replace("cartonized_", ""),
                    session["user"].get("email"),
                ),
            )
            try:
                connection.commit()
                session["user"] = {
                    "name": session["user"].get("name"),
                    "email": session["user"].get("email"),
                    "image": session["user"].get("image").replace("cartonized_", ""),
                }
            except Error as e:
                print(e.message)
        return redirect("profile")
    if not session["user"]:
        return redirect("login")
    return render_template("profile.html", title="Profile", user=session["user"])


if __name__ == "__main__":
    app.run(debug=True)
