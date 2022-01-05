import cv2
import sqlite3
import skimage.io as io
from sqlite3 import Error
from face_detection.classifier import *
from face_detection.face_detection import *
from cartonize.cartonize import cartoonize
from flask import Flask, render_template, request, redirect, session, jsonify


app = Flask(__name__)
app.name = "BRAW"
app.static_folder = "static"
app.secret_key = "65fa34c77b83f7114eea7b5c"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


DATABASE = "database.db"

names_to_emails = {
    "robert": "robertmounir66@gmail.com",
    "bishoy": "bishoyatef313@gmail.com",
    "abdullah": "abdullahadel.aam@gmail.com",
    "w2am": "weaam.ali99@eng-st.cu.edu.eg"
}


def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)

    print("CONNECTED SUCCESSFULLY TO DATABASE")
    return conn


def generate_frames(camera):
    faces = []
    d = 2
    q = 0
    o = 2

    old = ""
    occurrences = 0
    detected_user = None

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faces, frame, name, d, q, o = face_detection(
                faces, camera, d, q, o)
            if name:
                if occurrences == 0:
                    old = name
                    occurrences += 1
                elif name == old:
                    occurrences += 1
                else:
                    old = ""
                    occurrences = 0
                print(occurrences)
                print(old)
                if occurrences == 3:
                    detected_user = names_to_emails.get(name)
                    print(detected_user)
                    break

    return detected_user


@app.route("/")
def home():
    try:
        if session["user"]:
            return redirect("profile")
        return redirect("login")
    except:
        return redirect("login")


@app.route("/video")
def video():
    camera = cv2.VideoCapture(0)
    user = generate_frames(camera)
    camera.release()
    return user


@app.route("/login-ajax", methods=["POST"])
def login_ajax():
    # POST Method
    if request.method == "POST":
        email = request.json["email"]

        cur = get_db_connection().cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if user:
            session["user"] = {
                "name": user[2],
                "email": user[3],
                "image": user[5],
            }
            resp = jsonify(success=True)
            return resp

        resp = jsonify(success=False)
        resp.status_code = 404
        return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    # POST Method
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = get_db_connection().cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", (email,
                                                                     password)
        )
        user = cur.fetchone()
        if user:
            session["user"] = {
                "name": user[2],
                "email": user[3],
                "image": user[5],
            }
            return redirect("profile")

        return redirect("login")

    # GET Method
    if (session["user"]):
        return redirect('profile')
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
    return redirect("profile")


@app.route("/cartonize", methods=["GET", "POST"])
def cartonize():
    if request.method == "POST":
        if "cartonized_" not in str(session["user"].get("image")):
            originalImage = io.imread(
                "./static/images/" + str(session["user"].get("image"))
            )
            print(originalImage[:, :, 0:3].shape)
            cartonizedImage = cartoonize(originalImage[:, :, 0:3])
            io.imsave(
                "./static/images/cartonized_" +
                str(session["user"].get("image")),
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

    elif not session["user"]:
        return redirect("login")
    return redirect("profile")


if __name__ == "__main__":
    app.run(debug=True)
