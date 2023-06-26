from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from tempfile import mkdtemp
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from helper import *
from os import mkdir, listdir, path, rmdir
import json
import threading
import mysql.connector
import PyPDF2
import shutil
import time

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CSRF Token
app.config['SECRET_KEY'] = "eef5a3c7e71c3b66a00ec071825e39e1"
csrf = CSRFProtect(app)
csrf.init_app(app)

# Password Hash
bcrypt = Bcrypt(app)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pdflib"
)

sql = db.cursor(dictionary=True)

# Home Page
@app.route("/")
def index():
    return render_template("users/index.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Login Request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        sql.execute(
            "SELECT * FROM users WHERE username = %s", (username, ))
        row = sql.fetchone()

        if row:
            hashed_password = row["password"]
            if bcrypt.check_password_hash(hashed_password, password):
                session["user_id"] = 1
                session["is_admin"] = int(row["admin"])
                if session["is_admin"]:
                    print("Yes")
                return redirect("/")

        # Incorrect Credintials
        return render_template("users/login.html", error=True)
    # Login Page
    else:
        # If not Logged in
        if session.get("user_id") is None:
            return render_template("users/login.html")
        # User already Logged in
        else:
            return redirect("/")

# Register Page
@app.route("/register")
def register():
    return render_template("users/register.html")

# History Page
@app.route("/history")
def history():
    return render_template("users/history.html")

# Wishlist Page
@app.route("/wishlist")
def wishlist():
    return render_template("users/wishlist.html")

# Books Page
@app.route("/book/<sid>")
def book(sid):
    print(sid)
    return render_template("users/book.html", title="Hello world!", book=True)

# Admin Home Page
@app.route("/admin")
def admin():
    if session.get("user_id"):
        return render_template("admin/index.html")
    else:
        return redirect("/admin/login")

# Admin login Page
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    # Login Request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        sql.execute("SELECT * FROM users WHERE username = %s AND admin = 1", (username, ))
        row = sql.fetchone()

        if row:
            hashed_password = row["password"]
            if bcrypt.check_password_hash(hashed_password, password):
                session["user_id"] = 1
                session["is_admin"] = 1
                return redirect("/admin")
            
        # Incorrect Credintials
        return render_template("admin/login.html", error=True)
    # Login Page
    else:
        # If not Logged in
        if session.get("user_id") is None:
            return render_template("admin/login.html")
        # User already Logged in
        else:
            return redirect("/admin")

# Admin Add Book Page
@app.route("/admin/add", methods=["GET", "POST"])
def admin_add_book():
    if is_admin(session):
        if request.method == "POST":
            # User sent a file
            if len(request.files.getlist("file")):
                # Save File
                sid = generate_sid()
                file = request.files['file']
                mkdir(f"files/{sid}")
                file.save(f"files/{sid}/{sid}.pdf")

                # Check File Type
                if get_pages_num(sid) == 0:
                    time.sleep(1)
                    shutil.rmtree(f"files/{sid}")
                    return "404"

                # Start Converting
                convert = threading.Thread(target=pdf_convert, args=(sid,))
                convert.start()
                return sid
            
            # User sent Details form
            else:
                sid = request.form.get("sid")
                title = request.form.get("title")
                author = request.form.get("author")
                date = request.form.get("date")
                version = request.form.get("version")
                lang = request.form.get("lang")
                desc = request.form.get("description")

                # Check SID Validity
                if not Check.sid(sid, sql, "add"):
                    return "404"
                
                # Get file Size
                pages_num = get_pages_num(sid)
                file_size = get_file_size(sid)
                
                # Check Data And Send to Database
                if Check.title(title) and Check.author(author) and Check.date(date):
                    version = 0 if not Check.version(version) else version
                    lang = 0 if not Check.lang(lang) else lang
                    desc = "No description Available" if not Check.desc(desc) else desc

                    sql.execute("INSERT INTO books (sid, name, author, version, pub_date, lang, size, pages, admin) \
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                [sid, title, author, version, date, lang, file_size, pages_num, session["user_id"]])
                    
                    db.commit()

                    with open(f"files/{sid}/desc.txt", "w") as desc_file:
                        desc_file.write(desc)

                    return "200"
                return "404"
        return render_template("admin/add.html")
    return redirect("/admin/login")

# Admin Edit Book Page
@app.route("/admin/edit/<sid>", methods=["GET", "POST"])
def admin_edit_book(sid):
    if session.get("user_id"):
        if request.method == "POST":
            title = request.form.get("title")
            author = request.form.get("author")
            date = request.form.get("date")
            version = request.form.get("version")
            lang = request.form.get("lang")
            desc = request.form.get("description")

            # Check Data validity
            if Check.sid(sid, sql, "edit") and Check.title(title) and \
                Check.author(author) and Check.date(date) and \
                Check.version(version) and Check.version(lang) and Check.version(desc):
                    sql.execute("UPDATE books SET (name, author, version, pub_date, lang) \
                                = (%s, %s, %s, %s, %s) WHERE sid = %s",
                                [title, author, version, date, lang, sid])

                    db.commit()

                    with open(f"files/{sid}/desc.txt", "w") as desc_file:
                        desc_file.write(desc)

                    return "200"
            
            return "404"
        return render_template("admin/edit.html")
    return redirect("/admin/login")

# Converting Progress
@app.route("/admin/progress")
def admin_upload_progress():
    if is_admin(session):
        sid = request.args.get("sid")
        if path.exists(f"files/{sid}"):
            num = get_pages_num(sid)
            count = 0
            for file in listdir(f"files/{sid}"):
                # check if current path is a file
                if path.isfile(path.join(f"files/{sid}", file)) and ".svg" in file:
                    count += 1
            return json.dumps([count-1, num])
        
    return "404"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


