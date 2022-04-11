# Group 14 cloud_computing Coursework

A fun web app which allows users to generate random Owen Willson movies and rate them. Rating the moviews will add them to their own private user-specific lists which they can amend by changing scores and deleting entries. This webapp makes use of the Owen Wilson API: https://owen-wilson-wow-api.herokuapp.com/wows/random

Hopefully this project will make you go:
![Alt Text](https://thumbs.gfycat.com/GoodnaturedUglyGreendarnerdragonfly-max-1mb.gif)

# REST API Functions

The REST API is based on Python's Flask module and SQLAlchemy is used for object-relational mapping. The Google Cloud Platform is used to deploy the app and to home the persistent databases. 

This web app features:
1. User accounts (with personal user functions)
3. Hashed passwords
4. A Persistent cloud database ( usingGCP)
5. Dynamically generated REST API
6. makes use of an extral database API
7. Two Unique Datasets (Users and Movie_review)

# RESTful Services
#### 1 GET
The GET request is preformed when a the homepage is visited and when the WOW button is pressed. THis function gets a randomly generated owen wilson movie from the extral API.

HTML Form:

![image](https://user-images.githubusercontent.com/103308532/162691190-e1ce3a82-c061-4959-89e6-527495b674c9.png)

app.py handling of the GET method form:

![image](https://user-images.githubusercontent.com/103308532/162691549-794fef32-d889-4143-864c-2353ce32d15c.png)

#### 2 POST
The web app makes use of 3 POST operations.

The first POST operation is used to allow a user to create an account on the /signup/ route.
#### 3 PUT
#### 4 DELETE

# Setup
