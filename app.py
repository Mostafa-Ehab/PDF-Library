from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("users/index.html")

@app.route("/book/<sid>")
def book(sid):
    print(sid)
    return render_template("users/book.html", title="Hello world!")

@app.route("/history")
def history():
    return render_template("users/history.html")


@app.route("/wishlist")
def wishlist():
    return render_template("users/wishlist.html")

@app.route("/login")
def login():
    return render_template("users/login.html")


@app.route("/register")
def register():
    return render_template("users/register.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


