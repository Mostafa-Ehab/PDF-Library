from flask import Flask, render_template, session, redirect, request, abort, send_file
from flask_session import Session
from tempfile import mkdtemp
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from helper import *
from modules.register import Register
from os import mkdir, listdir, path
import json
import threading
import mysql.connector
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
    sql.execute("SELECT * FROM books")
    data = sql.fetchall()
    sql.execute("SELECT * FROM categories")
    categories = sql.fetchall()
    return render_template("users/index.html", data=data, categories=categories, logged_in=is_logged_in(session))

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Login Request
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        sql.execute(
            "SELECT * FROM users WHERE username = %s", [username])
        row = sql.fetchone()

        if row:
            hashed_password = row["password"]
            if bcrypt.check_password_hash(hashed_password, password):
                session["user_id"] = 1
                session["is_admin"] = int(row["admin"])
                if session["is_admin"]:
                    print("This user is admin")
                return redirect("/")

        # Incorrect Credintials
        return render_template("users/login.html", error=True, msg="Incorrect username or Password")
    # Login Page
    else:
        # If not Logged in
        if not is_logged_in(session):
            return render_template("users/login.html")
        # User already Logged in
        else:
            return redirect("/")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    register = Register(sql, db, bcrypt)
    return register.register()

# History Page
@app.route("/history")
def history():
    if is_logged_in(session):
        sql.execute("SELECT books.* FROM books RIGHT JOIN history ON books.id = history.book_id WHERE \
                    history.user_id = %s ORDER BY history.last_date DESC", [session['user_id']])
        data = sql.fetchall()
    else:
        data = []

    sql.execute("SELECT * FROM categories")
    categories = sql.fetchall()
    return render_template("users/history.html", data=data, categories=categories, logged_in=is_logged_in(session))

# Wishlist Page
@app.route("/wishlist")
def wishlist():
    sql.execute("SELECT * FROM categories")
    categories = sql.fetchall()
    return render_template("users/wishlist.html", categories=categories, logged_in=is_logged_in(session))

# Books Page
@app.route("/book/<sid>")
def book(sid):
    if Check.sid(sid, sql, "edit"):
        sql.execute("SELECT * FROM books WHERE sid = %s", [sid])
        row = sql.fetchone()

        if is_logged_in(session):
            add_history(db, sql, session["user_id"], row['id'])

        return render_template("users/book.html", data=row, book=True, logged_in=is_logged_in(session))
    return abort(404)

@app.route("/book/<sid>/<num>.svg")
def book_img(sid, num):
    file_name = f"files/{sid}/{num}.svg"
    if path.exists(file_name):
        return send_file(file_name)
    return abort(404)
    

@app.route("/book/<sid>/<name>.pdf")
def book_pdf(sid, name):
    file_name = f"files/{sid}/{sid}.pdf"
    if path.exists(file_name):
        return send_file(file_name, download_name=f"{name}.pdf" ,as_attachment=True)
    return abort(404)

@app.route("/category/<category_id>")
def category(category_id):
    sql.execute("SELECT * FROM categories WHERE id = %s", [category_id])
    row = sql.fetchone()
    if row:
        sql.execute("SELECT * FROM books WHERE id IN (SELECT book_id FROM \
                    classification WHERE category_id = %s)", [category_id])
        data = sql.fetchall()

        sql.execute("SELECT * FROM categories")
        categories = sql.fetchall()
        return render_template("users/index.html", data=data, categories=categories, logged_in=is_logged_in(session))

# Admin Home Page
@app.route("/admin")
def admin():
    if is_admin(session):
        sql.execute("SELECT * FROM books")
        data = sql.fetchall()

        sql.execute("SELECT * FROM categories")
        categories = sql.fetchall()

        return render_template("admin/index.html", data=data, categories=categories)
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
        if not is_admin(session):
            session.clear()
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
                category = request.form.getlist("category")
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
                    
                    book_id = sql.lastrowid

                    for cat in category:
                        sql.execute("SELECT * FROM categories WHERE id = %s", [cat])
                        if sql.fetchone():
                            sql.execute("INSERT INTO classification VALUES (%s, %s)", [book_id, cat])
                            db.commit()
                        else:
                            return "404"

                    with open(f"files/{sid}/desc.txt", "w") as desc_file:
                        desc_file.write(desc)

                    return "200"
                return "404"
        else:
            sql.execute("SELECT * FROM languages")
            languages = sql.fetchall()

            sql.execute("SELECT * FROM categories")
            categories = sql.fetchall()

            return render_template("admin/add-book.html", languages=languages, categories=categories)
    return redirect("/admin/login")

# Admin Edit Book Page
@app.route("/admin/edit/<sid>", methods=["GET", "POST"])
def admin_edit_book(sid):
    if is_admin(session):
        if request.method == "POST":
            title = request.form.get("title")
            author = request.form.get("author")
            date = request.form.get("date")
            version = request.form.get("version")
            lang = request.form.get("lang")
            category = request.form.getlist("category")
            desc = request.form.get("description")

            # Check Data validity
            if Check.sid(sid, sql, "edit") and Check.title(title) and \
                Check.author(author) and Check.date(date) and \
                Check.version(version) and Check.version(lang) and Check.version(desc):
                    sql.execute("SELECT id FROM books WHERE sid = %s", [sid])
                    book_id = sql.fetchone()['id']

                    category = [int(i) for i in category]
                    
                    sql.execute("SELECT category_id FROM classification WHERE book_id = %s", [book_id])
                    old_categories = sql.fetchall()
                    old_categories = [int(i['category_id']) for i in old_categories]

                    print(category)
                    print(old_categories)

                    add = [i for i in category if i not in old_categories]
                    for i in add:
                        sql.execute("INSERT INTO classification VALUES (%s, %s)", [book_id, i])
                        db.commit()

                    remove = [i for i in old_categories if i not in category]
                    for i in remove:
                        sql.execute("DELETE FROM classification WHERE book_id = %s AND category_id = %s", [book_id, i])
                        db.commit()

                    sql.execute("UPDATE books SET name = %s, author = %s, version = %s, \
                                pub_date = %s, lang = %s WHERE sid = %s",
                                [title, author, version, date, lang, sid])

                    db.commit()

                    with open(f"files/{sid}/desc.txt", "w") as desc_file:
                        desc_file.write(desc)

                    return redirect("/admin")
            return abort(404)
        else:
            if Check.sid(sid, sql, "edit"):
                sql.execute("SELECT * FROM books WHERE sid = %s", [sid])
                row = sql.fetchone()
                row['desc'] = open(f"files/{sid}/desc.txt", "r").read()

                sql.execute("SELECT * FROM categories")
                categories = sql.fetchall()

                sql.execute("SELECT category_id FROM classification WHERE book_id = %s", [row['id']])
                selected = [i['category_id'] for i in sql.fetchall()]

                return render_template("admin/edit.html", data=row, categories=categories, selected=selected)
            return abort(404)
    return redirect("/admin/login")

@app.route("/admin/delete/<sid>")
def delete_book(sid):
    if is_admin(session):
        if Check.sid(sid, sql, "edit"):
            sql.execute("DELETE FROM books WHERE sid = %s", [sid])
            db.commit()
            shutil.rmtree(f"files/{sid}")

            return redirect("/admin")
        else:
            return abort(404)
    else:
        return abort(404)

@app.route("/admin/category")
def admin_categories():
    if is_admin(session):
        sql.execute("SELECT categories.*, COUNT(classification.book_id) AS num FROM categories JOIN classification ON categories.id = classification.category_id GROUP BY (classification.category_id)")
        data = sql.fetchall()
        print(data)

        return render_template("admin/categories.html", data=data, categories=data)
    else:
        return redirect("/admin/login")

@app.route("/admin/category/add", methods=["POST", "GET"])
def admin_add_category():
    if is_admin(session):
        if request.method == "POST":
            name = request.form.get("name")
            books = request.form.getlist("add")

            if not name:
                return "Please Check your inputs"
            
            sql.execute("SELECT * from categories WHERE name = %s", [name])
            row = sql.fetchone()

            if row:
                return "This category already exist, please go to categories page"
            
            sql.execute("INSERT INTO categories (name) VALUES (%s)", [name])
            db.commit()

            category_id = sql.lastrowid
            print(category_id)

            for book_id in books:
                sql.execute("INSERT INTO classification VALUES (%s, %s)",
                            [book_id, category_id])
                db.commit()

            return "200"
        else:
            sql.execute("SELECT * FROM books")
            data = sql.fetchall()

            sql.execute("SELECT * FROM categories")
            categories = sql.fetchall()

            return render_template("admin/add-category.html", data=data, categories=categories)
    else:
        return redirect("/admin/login")

@app.route("/admin/category/<category_id>", methods=["POST", "GET"])
def admin_edit_category(category_id):
    if is_admin(session):
        sql.execute("SELECT * from categories WHERE id = %s", [category_id])
        row = sql.fetchone()
        if row:
            if request.method == "POST":
                name = request.form.get("name")
                selected = request.form.getlist("add")
                selected = [int(i) for i in selected]

                if not name:
                    return "Please Check your inputs"

                sql.execute("SELECT * FROM categories WHERE name = %s", [name])

                if len(sql.fetchall()) != 0 and name != row['name']:
                    return "This category already exist, please go to categories page"
                
                else:
                    sql.execute("UPDATE categories SET name = %s WHERE id = %s", [name, category_id])
                    db.commit()

                sql.execute("SELECT id FROM books WHERE id IN (SELECT book_id FROM \
                            classification WHERE category_id = %s)", [category_id])
                books = sql.fetchall()
                books = [i['id'] for i in books]

                add = [i for i in selected if i not in books]
                for i in add:
                    sql.execute("INSERT INTO classification VALUES (%s, %s)", [i, category_id])
                    db.commit()

                remove = [i for i in books if i not in selected]
                for i in remove:
                    sql.execute("DELETE FROM classification WHERE (book_id = %s AND category_id = %s)",
                                [i, category_id])
                    db.commit()
                
                return "200"
            else:
                sql.execute("SELECT * FROM books WHERE id IN (SELECT book_id FROM \
                            classification WHERE category_id = %s)", [category_id])
                selected = sql.fetchall()

                sql.execute("SELECT * FROM books WHERE id NOT IN (SELECT book_id FROM \
                            classification WHERE category_id = %s)", [category_id])
                not_selected = sql.fetchall()

                sql.execute("SELECT * FROM categories")
                categories = sql.fetchall()

                return render_template("admin/edit-category.html", category=row, selected=selected, not_selected=not_selected, categories=categories)
        return abort(404)
    else:
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


