from flask import Flask, render_template, request, redirect, session, flash
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ThisIsSecret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
  session["errors"] = 0
  return render_template("index.html")

@app.route("/complete", methods=["POST"])
def complete():
  session["reconfirm"] = request.form["pw_reconfirm"]
  if session["password"] != session["reconfirm"]:
    flash("Your password didn't match our records.")
  else:
    session["errors"] = 10
  return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
  present = datetime.now()
  date_format = "%Y-%m-%d"
  birthdate = datetime.strptime(request.form["bday"], date_format)
  errors = 0
  if len(request.form["first_name"]) < 1 or len(request.form["last_name"]) < 1 or len(request.form["email"]) < 1 or len(request.form["password"]) < 1 or len(request.form["pw_confirm"]) < 1:
    flash("Fields cannot be empty!")
  else:
    errors += 1
  if not request.form["first_name"].isalpha() or not request.form["last_name"].isalpha():
    flash("Only letters allowed for first and last name")
  else:
    errors += 1
  if not EMAIL_REGEX.match(request.form['email']):
    flash("Invalid Email Address!")
  else:
    errors += 1
  if birthdate > present:
    flash("Birth date must be a past date")
  else:
    errors += 1
  if len(request.form["password"]) < 8:
    flash("Password must be at least 8 characters")
  else:
    errors += 1
  if request.form["password"] != request.form["pw_confirm"]:
    flash("Password didn't match confirmation. Please try again.")
  else:
    errors += 1
  if errors == 6:
    flash("Thank you for registering")
  session["first_name"] = request.form["first_name"]
  session["last_name"] = request.form["last_name"]
  session["email"] = request.form["email"]
  session["bday"] = request.form["bday"]
  session["password"] = request.form["password"]
  session["pw_confirm"] = request.form["pw_confirm"]
  session["errors"] = errors
  print "all data received"
  return render_template("index.html")


app.run(debug=True)