from flask import Flask, render_template,request
import sqlite3

app = Flask(__name__)

def create_db():
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            author TEXT,
            status TEXT
        )
    """)

    con.commit()
    con.close()

create_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/books")
def books():
    return render_template("books.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]
        status = request.form["status"]

        con = sqlite3.connect("library.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO books (name, author, status) VALUES (?, ?, ?)",
            (name, author, status)
        )

        con.commit()
        con.close()

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)