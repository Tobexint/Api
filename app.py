from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    #
    person_list = Person.query.all()
    return render_template('index.html', person_list=person_list)

@app.route("/add", methods=["POST"])
def add():
    # add new person
    name = request.form.get("name")
    new_person = Person(name=name, complete=False)
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<name>")
def update(person_name):
    person = Person.query.filter_by(name=person_name).first()
    person.complete = not person.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<name>")
def delete(person_name):
    person = Person.query.filter_by(name=person_name).first()
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    #db.create_all()

    #new_todo = Todo(title="todo 1", complete=False)
    #db.session.add(new_todo)
    #db.session.commit()

    app.run(debug=True)

