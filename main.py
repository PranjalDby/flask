from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from database import exec_db


app = Flask(__name__)
app.secret_key = os.getenv(key="SECRET_KEY")


# regex_for validation

NAME_REGEX = re.compile(r"^[A-Za-z ]{2,50}$")
ADDRESS_REGEX = re.compile(r"^[A-Za-z0-9\s,./#-]{10,200}$")

# example User
USER = {"username": "admin", "password": generate_password_hash("password123")}


@app.route("/")
def hello_main():
    return render_template("static.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER["username"] and check_password_hash(
            USER["password"], password
        ):
            session["user"] = username
            return redirect(url_for("dashboard"))

        else:
            error = "Invalid Credentials"
            return render_template("error.html", error=error)

    return render_template("loginpage.html", error=error)

def is_valid_id(id_value):
    return (
    id_value.isdigit()
    and 6 <= len(id_value) <= 10
    and not id_value.startswith("0")
    )

@app.route("/dashboard", methods=["POST"])
def dashboard():
    __resp = None
    res = ''
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # connecting to postgres    
        filled_name = request.form.get("name").strip()
        filled_id = request.form.get("id").strip()
        filled_address = request.form.get("address").strip()
        
        if not NAME_REGEX.match(filled_name):
            error = "Name only containe Alphabets and spaces"
            
        elif not ADDRESS_REGEX.match(filled_address):
            error = "Invalid Address"
            
        elif not is_valid_id(filled_id):
            error = "Invalid ID Format"
            
        else:
            print('Inserting into DATABASE')
            QUERY = """INSERT INTO user_info VALUES(%s, %s, %s)"""
            exec_db(query=QUERY,params=(filled_id,filled_name,filled_address))
            
    return render_template("dashboard.html", user=session["user"],res=res)


@app.route("/about")
def aboutMe():
    return render_template("aboutMe.html")


if __name__ == "__main__":
    app.run(debug=True)
