import os
from flask import Flask, flash, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
from utilities import allowed_file, detectFace

UPLOAD_FOLDER = "uploads"

names = ["None", "Dharmaraj", "Vikram"]
app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

loggedin = None


def capture_by_frames():
    pass


@app.route("/")
def index():

        return render_template("index.html")
    return redirect("/signup", code=302)


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        firstname = request.form["first_name"]
        lastname = request.form["last_name"]
        username = request.form["user_name"]
        password = request.form["password"]
        email = request.form["email"]
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
            return redirect("/", code=302)
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)
