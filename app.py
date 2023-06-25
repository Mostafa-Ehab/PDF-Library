from flask import Flask, render_template

app = Flask(__name__)

# Home Page
@app.route("/")
def index():
    return render_template("users/index.html")

# Login Page


@app.route("/login")
def login():
    return render_template("users/login.html")

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
    return render_template("admin/index.html")

# Admin login Page
@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")

# Admin Add Book Page
@app.route("/admin/add")
def admin_add_book():
    return render_template("admin/add.html")

# Admin Edit Book Page
@app.route("/admin/edit/<sid>")
def admin_edit_book(sid):
    print(sid)
    return render_template("admin/edit.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


