from flask import request, render_template, session
from helper import *

class Register:
    def __init__(self, sql, db, bcrypt):
        self.sql = sql
        self.db = db
        self.bcrypt = bcrypt

    def register(self):
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            password_conf = request.form.get("password-conf")

            # Check email
            if email:
                if check_email(email):
                    self.sql.execute(
                        "SELECT * FROM users WHERE email = %s", [email])
                    row = self.sql.fetchone()
                    if row:
                        print(row)
                        return "This email already exist, try login instead"
                else:
                    return "Please enter a valid email"

            # Check username
            if username:
                self.sql.execute(
                    "SELECT * FROM users WHERE username = %s", [username])
                row = self.sql.fetchone()
                if row:
                    return "Username already exist, please choose another one"

            # Check that Either username or email exist
            if not username and not email:
                return "Please enter either username or email"

            # Check that passwords not empty
            if not password:
                return "Password can't be empty"

            # Check that passwords match
            if password != password_conf:
                return "Passwords don't match"

            return self.create_account(username, email, password)

        else:
            return render_template("users/register.html", register=True)
            
    def create_account(self, username, email, password):
        self.sql.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                         [username, email, self.bcrypt.generate_password_hash(password).decode('utf-8')])
        
        self.db.commit()
        session["user_id"] = 1

        return "200"
