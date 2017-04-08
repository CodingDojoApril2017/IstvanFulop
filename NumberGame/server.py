from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

import random

@app.route('/')
def index():
  session["secret"] = random.randrange(1, 101)
  print "secret is", session["secret"]
  session["guess"] = -1
  print "guess is", session["guess"]
  return render_template("index.html")

@app.route('/guess', methods=["POST"])
def guess():
  session['guess'] = int(request.form['userguess'])
  print "secret is", session["secret"]
  print "guess is", session["guess"]
  return render_template("index.html")


app.run(debug=True)