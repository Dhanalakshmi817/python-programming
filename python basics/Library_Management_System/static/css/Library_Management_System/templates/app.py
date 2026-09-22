from flask import Flask, render_template,request,redirect
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
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
    con = sqlite3.connect("library.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM books")

    data = cur.fetchall()
    con.close()

    return render_template("books.html", books=data)

@app.route("/members")
def members():
    con = sqlite3.connect("library.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM members")

    data = cur.fetchall()
    con.close()

    return render_template("members.html", members=data)

@app.route("/addmember", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        con = sqlite3.connect("library.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )

        con.commit()
        con.close()

    return render_template("addmember.html")

@app.route("/deletemember/<int:id>")
def delete_member(id):
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    cur.execute("DELETE FROM members WHERE id = ?", (id,))

    con.commit()
    con.close()

    return redirect("/members")

@app.route("/editmember/<int:id>", methods=["GET", "POST"]) 
def editmember(id):
     con = sqlite3.connect("library.db") 
     con.row_factory = sqlite3.Row 
     cur = con.cursor()
     if request.method == "POST": 
        name = request.form["name"] 
        email = request.form["email"]
        phone = request.form["phone"] 

        cur.execute( "UPDATE members SET name = ?, email = ?, phone = ? WHERE id = ?", (name, email, phone, id) )
        con.commit() 
        con.close() 

        return redirect("/members") 
     
     cur.execute( "SELECT * FROM members WHERE id = ?", (id,) )
     member = cur.fetchone() 
     con.close()

     return render_template("editmember.html", member=member)

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

@app.route("/deletebook/<int:id>")
def deletebook(id):

    con = sqlite3.connect("library.db")
    cur = con.cursor()

    cur.execute(
        "DELETE FROM books WHERE id = ?",
        (id,)
    )

    con.commit()
    con.close()

    return redirect("/books")

if __name__ == "__main__":
    app.run(debug=True)