# Overview

This is part 2 of my first project creating a web app. 

To prepare for this project I using HTML and did additional research in the Django docs. I was unsatisfied with where I left off and I wanted to see this project through. While it is still not complete I am proud of what I was able to learn and accomplish. 

Prior to this 2 part project I had no experience doing any kind of web dev. This acted as an effective introduction to html, web servers, and hosting as well as another project to further understand relational databases. 

[Web App Demo - YouTube](https://youtu.be/taToQf4DyPk)

# Web Pages

* Signin/Create New Account page - allows user to sign in and/or create account
* User home page - displays users saved tricks
* All tricks page - allows user to edit saved tricks
* Description page -  shows the description of the trick selected

# Database Tables

* Tricks - all of the tricks (built from API)
* User - username and password
* UserTricks - stores id for the user and the tricks they select
* Class - classification of tricks

# Development Environment

This app uses Django and Requests from Python and was developed with Visual Studio Code.

# Useful Websites

* [Tricking Database API](http://club540.com/api/tricks)
* [Similar website which I was attempting to emulate](http://www.club540.com/tricktionary)
* [Tutorial - RealPython.com](https://realpython.com/get-started-with-django-1/#add-bootstrap-to-your-app)
* [Django Docs](https://docs.djangoproject.com)
* [W3schools - HTML](https://www.w3schools.com/html)

# Future Work

### Recent revisions:
* Clear user's saved tricks (did not work in video demo but have fixed since)

### Future additions:
* Prepopulate checkmarks
* Unselect checkbox to remove saved tricks
* Random Combo Generator using saved tricks
