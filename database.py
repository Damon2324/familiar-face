import sqlite3


def addUser(firstname, lastname, password, linkedin, github, about, persona) -> int:
    conn = sqlite3.connect("profile.db")
    cursor = conn.cursor()
    qry = "INSERT into profile(id,firstname, lastname, password, linkedin, github, about, persona) VALUES(null,?,?,?,?,?,?,?)"
    cursor.execute(
        qry, (firstname, lastname, password, linkedin, github, about, persona)
    )

    data = cursor.execute("SELECT id FROM Profile")
    userid = data.lastrowid

    conn.commit()
    conn.close()

    return userid


def getData(userid):
    conn = sqlite3.connect("peofile.db")
    cursor = conn.cursor()
    qry = "SELECT * FROM profile WHERE id=?"
    data = cursor.execute(qry, userid)
    conn.commit()
    conn.close()
    return data
