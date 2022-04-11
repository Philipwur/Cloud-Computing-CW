# Group 14 Cloud Computing Coursework
Group Members:

Michael Capaldi - 210641428

Daniel Crake - 210744246

Philip Wurzner - 210930632

A fun web app which allows users to generate random Owen Willson movies and rate them. Rating the moviews will add them to their own private user-specific lists which they can amend by changing scores and deleting entries. This webapp makes use of the external Owen Wilson API: https://owen-wilson-wow-api.herokuapp.com/wows/random

Hopefully this project will make you go:
![Alt Text](https://thumbs.gfycat.com/GoodnaturedUglyGreendarnerdragonfly-max-1mb.gif)

# REST API Functions

The REST API is based on Python's Flask module and SQLAlchemy is used for object-relational mapping. The Google Cloud Platform is used to deploy the app and to home the persistent databases. 

This web app features:
1. User accounts (with personal user functions)
3. Hashed passwords
4. A Persistent cloud database (using GCP)
5. Dynamically generated REST API
6. Makes use of an extral database API
7. Two Unique Datasets (Users and Movie_review)

# RESTful Services
#### 1 GET
The GET request is preformed when a the homepage is visited and when the WOW button is pressed. THis function gets a randomly generated owen wilson movie from the extral API.

HTML Form on the homepage:

![image](https://user-images.githubusercontent.com/103308532/162691190-e1ce3a82-c061-4959-89e6-527495b674c9.png)

app.py handling of the GET method form:

![image](https://user-images.githubusercontent.com/103308532/162691549-794fef32-d889-4143-864c-2353ce32d15c.png)

#### 2 POST
The web app makes use of 3 POST operations.

The first POST operation is used to allow a user to create an account on the /signup/ route.

HTML form (signup):

![image](https://user-images.githubusercontent.com/103308532/162698690-7ea7df2d-f053-4be3-9bcb-ebff6df0ab52.png)

app.py handling of the User Signup POST:

![image](https://user-images.githubusercontent.com/103308532/162698917-5dbffd16-40d6-4ff3-ab18-541b5b95db26.png)

the second POST operation is to allow a user to login:

HTML form (login):

![image](https://user-images.githubusercontent.com/103308532/162699911-dd31ac5f-bbee-4850-8160-1909ed8c2858.png)

app.py handling of the User Login POST:

![image](https://user-images.githubusercontent.com/103308532/162699944-3aff31e0-004a-45e8-8544-199a072a892f.png)

the final POST operation is to allow a user to post a review to their list:

HTML form (homepage):

![image](https://user-images.githubusercontent.com/103308532/162700389-38e8b46e-11ad-4305-a12a-80ab6cd1f3ab.png)

app.py handling of post request:

![image](https://user-images.githubusercontent.com/103308532/162700493-9af7349e-417e-49b3-9367-3c1c86bf30e2.png)

#### 3 PUT

One PUT request is present to allow for the editing of personal list entries.

HTML form (homepage):

![image](https://user-images.githubusercontent.com/103308532/162700663-10dfe623-ff48-4755-8aed-d6bcff10129c.png)

app.py handling:

![image](https://user-images.githubusercontent.com/103308532/162700734-466ded9a-fb9b-4f37-84f1-a7b6476ff287.png)

#### 4 DELETE

One DELETE request is present to allow for the removal of personal list entries.

HTML form (homepage):

![image](https://user-images.githubusercontent.com/103308532/162700890-4af6ec77-bea2-422a-b2ec-dc129fba4f9a.png)

app.py handling:

![image](https://user-images.githubusercontent.com/103308532/162700991-90052ee3-4a62-4373-87c7-29757999ab99.png)

# Setup
