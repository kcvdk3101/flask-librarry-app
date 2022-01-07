from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

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
  if request.method == "POST":
    title = request.form["title"]
    desc = request.form["description"]

    con = get_db()
    c = con.cursor()

    query = "INSERT INTO Library VALUES('{}', '{}')".format(title, desc)

    c.execute(query)
    con.commit()

    return redirect(url_for('home'))

  return render_template('new_item.html')


def get_db():
  # Check connection to database by G Object
  db = getattr(g, "_database", None)

  if db is None:
    db = g._database = sqlite3.connect(currentDirectory + "\library.db")
  
  return db


if __name__ == "__main__":
  app.run()