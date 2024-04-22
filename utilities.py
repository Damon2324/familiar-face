from linkedin_api import Linkedin
import requests as req
import cv2
import sys


def getLinkedInProfile(profileid) -> list:
    password = open("secret.key").read()
    api = Linkedin("aizensosukesama106@gmail.com", password)

    profile = api.get_profile("swarup-vishwas-8895221b9")

    recent_post = api.get_profile_posts("swarup-vishwas-8895221b9")

    print(recent_post)

    return [profile, recent_post]


def getGithubData(profileid) -> list:
    data = req.get(f"https://api.github.com/users/{profileid}")
    projects = req.get(
        f"https://api.github.com/users/{profileid}/repos?sort=created&direction=desc"
    )
    return [data, projects]


def detectFace(imagePath) -> int:

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30)
    )

    return len(faces)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
