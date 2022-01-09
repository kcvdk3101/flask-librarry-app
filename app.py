import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

class NewItemForm(FlaskForm):
  title = StringField("Title")
  description = TextAreaField("Description")
  submit = SubmitField("Submit")


@app.route('/', methods=["GET"])
def home():
  try:
    if request.method == "GET":
      con = get_db()
      c = con.cursor()

      query = "SELECT * from Library"
      result = c.execute(query)
      cards = result.fetchall()

      return render_template('home.html', cards=cards)
  except:
   return render_template('home.html')

# CRUD
@app.route('/item/new', methods=["GET", "POST"])
def new_item():
  con = get_db()
  c = con.cursor()
  form = NewItemForm()

  if request.method == "POST":
    title = form.title.data
    desc = form.description.data

    query = "INSERT INTO Library VALUES('{}', '{}')".format(title, desc)

    c.execute(query)
    con.commit()

    flash("Item {} has been submitted.".format(title), "success")

    return redirect(url_for('home'))

  return render_template('new_item.html', form=form)

# Connect to Database
def get_db():
  # Check connection to database by G Object
  db = getattr(g, "_database", None)

  if db is None:
    db = g._database = sqlite3.connect(currentDirectory + "\library.db")
  
  return db

# Close database connection
@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, "_database", None)

  if db is not None:
    db.close()


if __name__ == "__main__":
  app.run()