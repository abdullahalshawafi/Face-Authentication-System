import cv2
import sqlite3
import skimage.io as io
from sqlite3 import Error
from face_detection.classifier import *
from face_detection.face_detection import *
from cartonize.cartonize import cartoonize
from flask import Flask, render_template, request, redirect, session, Response


app = Flask(__name__)
app.name = "BRAW"
app.static_folder = "static"
app.secret_key = "65fa34c77b83f7114eea7b5c"
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


def generate_frames(camera):
    faces = []
    d = 2

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faces, d, frame = face_detection(faces, d, camera)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def home():
    try:
        if session["user"]:
            return redirect("profile")
    except:
        return redirect("login")


@app.route("/video")
def video():
    camera = cv2.VideoCapture(0)
    return Response(
        generate_frames(camera), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


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
    return redirect("profile")


@app.route("/cartonize", methods=["GET", "POST"])
def cartonize():
    if request.method == "POST":
        if "cartonized_" not in str(session["user"].get("image")):
            originalImage = io.imread(
                "./static/images/" + str(session["user"].get("image"))
            )
            print(originalImage[:,:,0:3].shape)
            cartonizedImage = cartoonize(originalImage[:,:,0:3])
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

    elif not session["user"]:
        return redirect("login")
    return redirect("profile")


if __name__ == "__main__":
    app.run(debug=True)
