import os
from flask import Flask, flash, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
from database import addUser
from utilities import allowed_file, detectFace, getPersona
import variables

UPLOAD_FOLDER = "uploads"

names = ["None", "Dharmaraj", "Vikram"]
app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def capture_by_frames():
    pass


@app.route("/profile/<int:userid>")
def get_profile():
    if variables.loggedin is None:
        return redirect("/signup", code=302)
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if variables.loggedin is not None:
        return redirect("/", code=302)

    if request.method == "POST":
        firstname = request.form["first_name"]
        lastname = request.form["last_name"]
        password = request.form["password"]
        linkedin = request.form["linked_url"]
        github = request.form["git_url"]
        about = request.form["about_user"]

        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]

        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            complete_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(complete_path)
            faces = detectFace(complete_path)
            if faces > 1:
                return redirect(request.url)

            if faces == 0:
                return redirect(request.url)

            print(faces)

            persona = getPersona(about)

            userid = addUser(
                firstname, lastname, password, linkedin, github, about, persona
            )

            extension = file.filename.split(".")[-1]

            os.rename(
                complete_path,
                os.path.join(
                    app.config["UPLOAD_FOLDER"], (str(userid) + "." + extension)
                ),
            )

            variables.loggedin = userid
            return redirect("/", code=302)
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)
