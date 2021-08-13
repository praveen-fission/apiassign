# CMS

This is a content management system where one can register and login.
Users can create, view, edit and delete their posts
.

## Installation

This project requires the following tools

Python - The programming language used by Flask

Sqlite - A relational database system

Sqlalchemy - It's a library for handling databases
 
Virtualenv - A tool for creating isolated Python environments.



To get started, install Python and flask on your local computer 
if you don't have them already. You can optionally use another database system instead of SQLite, like Postgres

## Create a virtual environment

```bash
python -m venv env
```
### To activate virtual environment

```bash
.\env\Scripts\activate
```

## Setup your database


You need to be able to connect to a database.
You will need to know the connection URL for your application which we will call DATABASE_URL in your environment variables. Here is an example:

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
```

```bash
from app import db
```

```bash
db.create_all()
```
## Register
[http://localhost:5000/User](http://localhost:5000/User)

## Login

[http://localhost:5000/login](http://localhost:5000/login)

## Post
[http://localhost:5000/content](http://localhost:5000/content)

## Get
[http://localhost:5000/Users](http://localhost:5000/Users)

## Put
[http://localhost:5000/epost](http://localhost:5000/epost)

## Delete
[http://localhost:5000/post](http://localhost:5000/post)
