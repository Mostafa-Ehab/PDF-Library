from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("users/index.html")

@app.route("/book/<sid>")
def book(sid):
    print(sid)
    return render_template("users/book.html", title="Hello world!")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


