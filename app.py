from flask import Flask, render_template, request, jsonify, json, url_for, abort, redirect, session,flash
import requests
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from userDB.setupDB import user
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)

class user(db.Model):
  
  __table_name__ = "user"
  
  u_id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
  
  user_name = db.Column(db.String(100), 
                       unique=True, 
                       nullable=False)
  
  pass_hash = db.Column(db.String(100), 
                        nullable=False)

  def __repr__(self):
    return '' % self.u_id

class movie_review(db.model):
  
  __table_name__ = "movie_review"
  
  l_id = db.Column(db.Integer, 
                   autoincrement=True,
                   primary_key=True)
  
  u_id = db.Column(db.Integer,
                       db.ForeignKey("user.u_id"))
  
  movie_name = db.Column(db.String(100), 
                         nullable=False)
  
  director = db.Column(db.String(100), 
                       nullable=False)
  
  year = db.Column(db.Integer(4),
                   nullable=False)
  
  score = db.Column(db.Float,
                   nullable=False)
  
  user = db.relationship("user", backref = db.backref("movie_review"))
  
  __table_args__ = {db.UniqueConstraint("movie_name", "u_id")}
  
  def __repr__(self):
    return '' % (self.l_id, self.u_id)
  

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = user(user_name=username, pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = user.query.filter_by(user_name=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("user_home", username=username))
            flash("Invalid username or password.")

    return render_template("login_form.html")

@app.route("/user/<username>/", methods = ["GET", "POST"])
def user_home(username):
    if request.method == "GET":
        url = "https://owen-wilson-wow-api.herokuapp.com/wows/random"
        resp = requests.get(url)
        response = resp.json()
        movie = response[0].get('movie')
        director = response[0].get('director')
        year = response[0].get('year')
        
    if request.method == "POST":
        
        rating = request.form["rating"]
        if not (rating):
            flash("rating cannot be empty")
            
        list_entry = movie_review(movie_name = movie,
                                director = director,
                                year = year,
                                score = rating)
        
        db.session.add(list_entry)
        db.session.commit()
        user_list = movie_review.query.filter_by(u_id=u_id).all()

    return render_template("user_home.html", username=username, movie=movie, director=director, year=year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
