from flask import Flask, render_template, request, jsonify, json, url_for, abort, redirect, session,flash
import requests
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '{Your Secret Key}'

db = SQLAlchemy(app)

'''
Class for the user registry/db 
Columns include username and password
Functions for:
-Finding whether a user exists, 
-Generating a password hash
-Verifing password hash
'''
class User(db.Model):
  
  u_id = db.Column(db.Integer, 
                   primary_key=True)
  
  username = db.Column(db.String(64), 
                       nullable=False)
  
  password = db.Column(db.String(64),
                      nullable=True)
  @classmethod
  def find_user(cls, username):
    return cls.query.filter_by(username = username).first()
  
  def generate_pass_hash(self, password):
    self.password = generate_password_hash(password)
  
  def check_pass(self, _password):
    return check_password_hash(self.password, _password)

'''
Class for the movie review registry/db 
Columns include username, movie name, director, year and score/review
Functions for:
-Finding whether a review by a user exists, 
-Generating a list with all movies reviewed by a user
'''
class Movie_review(db.Model):

  l_id = db.Column(db.Integer, 
                   primary_key=True)
  
  username = db.Column(db.String(64))
  
  movie = db.Column(db.String(64))
  
  director = db.Column(db.String(64))
  
  year = db.Column(db.Integer)
  
  review = db.Column(db.Float(10))
  
  @classmethod
  def find_review(cls, username, movie):
      return cls.query.filter_by(username = username, movie = movie).first()
    
  @classmethod
  def show_list(cls, username):
      return cls.query.filter_by(username = username)

'''
Signing-up REST
Post request collects username and password,
determines whether the username has been taken or whether the fields are empty
generates password hash and appends user to the database. 
'''
@app.route("/signup/", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if User.find_user(username = username) or not (username and password):
            flash("Username already Exists")
        else:
          new_user = User(username = username)
          new_user.generate_pass_hash(password = password)
          db.session.add(new_user)
          db.session.commit()
          flash("User added")
          return redirect(url_for("login"))
        
    return render_template("signup.html")

'''
logging-in REST
Post request collects username and password,
checks the user database for the username, and then compares the 
password hash to the verified hash of the inserted password
'''
@app.route("/", methods=["POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        login_user = User.find_user(username = username)
        
        if login_user and login_user.check_pass(_password = password):
            session[username] = True
            return redirect(url_for("user_home", username = username))
        else:
            flash("Invalid login")

    return render_template("login_form.html")

'''
Home Page REST

The home page makes use of the owen wilson wow api to randomly generate
a movie that owen willson plays in, along with the details of the movie.
the GET request connects to this external API and collects a random owen movie's details.

the first POST request allows the user to add the randomly generated movie, 
along with a score, to their list of reviewed movies. 

The second POST request acts as a PUT, and allows the user to change the score of 
a movie they have previously rated

The third POST request acts as a DELETE, and allows the user to remove their 
review entry from their list and the website database. 
'''
@app.route("/user/<username>/", methods = ["GET", "POST"])
def user_home(username):
  
    user_list = Movie_review.show_list(username = username)
    
    if request.method == "GET":
        url = "https://owen-wilson-wow-api.herokuapp.com/wows/random"
        resp = requests.get(url)
        response = resp.json()
        movie = response[0].get('movie')
        director = response[0].get('director')
        year = response[0].get('year')
        
    if request.method == "POST" and "rating" in request.form:
        
        movie = request.form['movie']
        director = request.form['director']
        year = request.form['year']
        score = request.form['rating']
        
        review = Movie_review(username = username,
                              movie = movie,
                              director = director,
                              year = year,
                              review = score)
        
        if Movie_review.find_review(username=username, movie=movie):
            flash("you have already reviewed this movie")

        else:
          db.session.add(review)
          db.session.commit()
          return redirect(url_for("user_home", username = username))
        
    if request.method == "POST" and "new_rating" in request.form:
      
        new_score = request.form['new_rating']
        movie = request.form['movie']
        movie_review = Movie_review.find_review(username = username, 
                                                movie = movie)
        movie_review.review = new_score
        db.session.commit()
        return redirect(url_for("user_home", username = username))
      
    if request.method == "POST" and "delete_request" in request.form:
      
        delete_request = request.form['delete_request']
        delete_review = Movie_review.find_review(username = username, 
                                                 movie = delete_request)
        db.session.delete(delete_review)
        db.session.commit()
        return redirect(url_for("user_home", username = username))
      
    return render_template("user_home.html", 
                           username = username, 
                           movie = movie, 
                           director = director, 
                           year = year, 
                           user_list = user_list)

@app.before_first_request
def create_tables():
    db.create_all()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
