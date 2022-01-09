import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length


app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

class NewItemForm(FlaskForm):
  title = StringField("Title",validators=[
    InputRequired("Input is required!"), 
    DataRequired("Data is required!"),
    Length(min=5, max=20, message="Input must be between 5 and 20 characters long")], 
  )
  price = DecimalField("Price")
  description = TextAreaField("Description",validators=[
    InputRequired("Input is required!"), 
    DataRequired("Data is required!"),
    Length(min=1, max=40, message="Input must be between 1 and 40 characters long")])
  category = SelectField("Category")
  subcategory = SelectField("Subcategory")
  submit = SubmitField("Submit")


@app.route("/")
def home():
  conn = get_db()
  c = conn.cursor()

  items_from_db = c.execute("""SELECT
                  i.id, i.title, i.description, i.price, i.image, c.name, s.name
                  FROM
                  items AS i
                  INNER JOIN categories     AS c ON i.category_id     = c.id
                  INNER JOIN subcategories  AS s ON i.subcategory_id  = s.id
                  ORDER BY i.id DESC
  """)

  items = []
  for row in items_from_db:
      item = {
          "id": row[0],
          "title": row[1],
          "description": row[2],
          "price": row[3],
          "image": row[4],
          "category": row[5],
          "subcategory": row[6]
      }
      items.append(item)

  return render_template("home.html", items=items)


# CRUD
@app.route('/item/new', methods=["GET", "POST"])
def new_item():
  con = get_db()
  c = con.cursor()
  form = NewItemForm()

  c.execute("SELECT id, name FROM categories")
  categories = c.fetchall()
  form.category.choices = categories

  c.execute("""SELECT id, name FROM subcategories
                WHERE category_id = ?""",
    (1,)
  )
  subcategories = c.fetchall()
  form.subcategory.choices = subcategories

  if form.validate_on_submit():
    # Process the form data
    c.execute("""INSERT INTO items
                (title, description, price, image, category_id, subcategory_id)
                    VALUES (?,?,?,?,?,?)""",
      ( 
          form.title.data,
          form.description.data,
          float(form.price.data),
          "",
          form.category.data,
          form.subcategory.data
      )
    )
    con.commit()

    flash("Item {} has been submitted.".format(request.form.get("title")), "green")

    return redirect(url_for('home'))

  if form.errors:
    flash("{}".format(form.errors), "red")
  
  return render_template('new_item.html', form=form)

@app.route("/item/<int:item_id>")
def item(item_id):
    c = get_db().cursor()
    item_from_db = c.execute("""SELECT
                   i.id, i.title, i.description, i.price, i.image, c.name, s.name
                   FROM
                   items AS i
                   INNER JOIN categories AS c ON i.category_id = c.id
                   INNER JOIN subcategories AS s ON i.subcategory_id = s.id
                   WHERE i.id = ?""",
                   (item_id,)
    )
    row = c.fetchone()

    try:
        item = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "image": row[4],
            "category": row[5],
            "subcategory": row[6]
        }
    except:
        item = {}
        return render_template("item.html", item=item)
    return redirect(url_for("home"))


# Connect to Database
def get_db():
  # Check connection to database by G Object
  db = getattr(g, "_database", None)

  if db is None:
    db = g._database = sqlite3.connect("db/globomantics.db")
  
  return db

# Close database connection
@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, "_database", None)

  if db is not None:
    db.close()


if __name__ == "__main__":
  app.run()