from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm.collections import attribute_mapped_collection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)
    phone = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    pincode = db.Column(db.String(6), nullable = False)
    category = db.relationship('Content', backref = "categories", lazy = True,
                collection_class=attribute_mapped_collection('contentattributes'))

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}', '{self.pincode}')"

class Content(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    body = db.Column(db.String(300), nullable = False)
    summary = db.Column(db.String(60), nullable = False)
    tags = db.Column(db.String(100))
    file = db.Column(db.BLOB())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    relate = db.relationship('Categories', backref = "category", lazy = True)

    @property
    def contentattributes(self):
        return self.id, self.title, self.body, self.summary

    def __repr__(self):
        return f"Content('{self.title}' and '{self.body}' and '{self.summary}')"

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cat1 = db.Column(db.String(20))
    cat2 = db.Column(db.String(20))
    cat3 = db.Column(db.String(20))
    cat_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable = False)

    def __repr__(self):
        return f"Categories('{self.cat1}' and '{self.cat2}' and '{self.cat3}')"

@app.route('/login', methods = ['POST'])
def login():
    fullname = request.json["fullname"]
    password = request.json["password"]
    all_users = User.query.all()
    for user in all_users:
        if(user.fullname == fullname and user.password == password):
            user = User.query.filter_by(fullname = fullname).first()
            contents_of_a_user = user.category
            contents = []
            for user in contents_of_a_user:
                result = {}
                result['title'] = user[1]
                result['body'] = user[2]
                result['summary'] = user[3]
                contents.append(result)
            return jsonify(contents)
    message = 'Invalid fullname or password.'
    return jsonify({"message": message})

@app.route('/category/<int:id>', methods = ['POST'])
def category(id):
    content = Content.query.filter_by(id = id).first()
    if(content):
        cat1 = request.json['cat1']
        cat2 = request.json['cat2']
        cat3 = request.json['cat3']
        cats = Categories(cat1 = cat1, cat2 = cat2, cat3 = cat3, cat_id = content.id)
        db.session.add(cats)
        db.session.commit()
        return jsonify({"cat1": cat1, "cat2": cat2, "cat3": cat3})
    else:
        message = 'cannot add categories'
        return jsonify({"message": message})

@app.route('/categories/<int:id>', methods = ['GET'])
def categories(id):
    cont = Content.query.filter_by(id = id).first()
    outer = []
    for cont in cont.relate:
        d={}
        d["cat1"] = cont.cat1
        d["cat2"]=cont.cat2
        d["cat3"]=cont.cat3
        outer.append(d)
    return jsonify(outer)

@app.route('/User', methods = ['POST'])
def User():
    fullname = request.json['fullname']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    country = request.json['country']
    pincode = request.json['pincode']
    error = None
    if(len(phone) != 10 and (char.isalpha() for char in phone)):
        error = 'phone number should be 10 digits and should not contain alphabets'
        return jsonify({"error":error})
    if(len(pincode) != 6 and (char.isalpha() for char in pincode)):
        error = 'pincode should be 6 digit and should not contain alphabets'
        return jsonify({"error": error})
    if(not email or not email.strip() or '@' not in email):
        error = 'please enter a valid email address'
        return jsonify({"error": error})
    if not(len(password) >= 8 and (any (char.isupper() for char in password) or any (char.islower() for char in password))):
        error = 'password should contain minimum 8 characters and an uppercase and lowercase character'
        return jsonify({"error": error})
    else:
        user = User(fullname = fullname, email = email, password = password, phone = phone,
                            address = address, city = city, state = state, country = country, pincode = pincode)

        db.session.add(user)
        db.session.commit()
        return jsonify({"fullname": fullname, "email": email, "password": password, "phone": phone, "address": address, "city": city, "state": state, "country": country, "pincode": pincode})

@app.route('/search/<string:fullname>', methods = ['GET','POST'])
def search(fullname):
    text_to_search = request.json['text_to_search']
    user = User.query.filter_by(fullname = fullname).first()
    for key,value in user.category.items():
        if(text_to_search in key):
            message = 'text found'
            return jsonify(text_to_search, message, key)
    message = 'not found'
    return jsonify({"message": message})

@app.route('/Users', methods = ['GET'])
def Users():
    users = User.query.all()
    output = []
    for user in users:
        result={}
        result["id"] = user.id
        result["fullname"]=user.fullname
        result["email"]=user.email
        result["password"] = user.password
        result["phone"] = user.phone
        result["address"] = user.address
        result["city"] = user.city
        result["state"] = user.state
        result["country"] = user.country
        result["pincode"] = user.pincode
        output.append(result)
    return jsonify(output)

@app.route('/posts/<int:id>', methods = ['GET'])
def posts(id):
    users = User.query.all()
    user1 = User.query.filter_by(id = id).first()
    list_of_ids = []
    for user in range(len(users)):
        list_of_ids.append(users[user].id)
    if(id in list_of_ids):
        output = []
        if(len(user1.category) == 0):
            message = 'there are no content for this user. Please add some content'
            return jsonify({"details":message})
        else:
            for content in user1.category:
                result={}
                result["id"] = content[0]
                result["title"]=content[1]
                result["body"]=content[2]
                result["summary"] = content[3]
                output.append(result)
            return jsonify(output)
    else:
        error = 'id is not registered in our database'
        return jsonify({"error": error})

@app.route('/contents/<int:id>', methods = ['GET'])
def contents(id):
    user1 = User.query.filter_by(id = id).first()
    output = []
    for user in user1.category:
        result={}
        result["title"] = user[0]
        result["body"] = user[1]
        result["summary"] = user[2]
        output.append(result)
    return jsonify(output)

@app.route('/content', methods = ['POST'])
def content():
    user = User.query.filter_by(fullname = request.authorization.get('username')).first()
    if(user and user.password == request.authorization.get('password')):
        title = request.form["title"]
        body = request.form["body"]
        summary = request.form["summary"]
        tags = request.form["tags"]
        pdf = request.files['pdf']
        data = pdf.read()
        cont  = Content(title = title, body = body, summary = summary, tags = json.dumps(tags), file = data ,user_id = user.id)
        db.session.add(cont)
        db.session.commit()
        return jsonify({"title":title, "body":body, "summary":summary, "tags": tags})
    else:
        return jsonify({"error": "try again"})

@app.route('/post/<int:id>', methods = ['DELETE'])
def post(id):
    user = User.query.filter_by(fullname = request.authorization.get('username')).first()
    if(user and user.password == request.authorization.get('password')):
        content = Content.query.get(id)
        output = []
        result = {}
        result['id'] = content.id
        result['title'] = content.title
        result['body'] = content.body
        result['summary'] = content.summary
        db.session.delete(content)
        db.session.commit()
        output.append(result)
        return jsonify(output)
    else:
        message = 'User credentials are incorrect'
        return jsonify({"message": message})

@app.route('/epost/<int:id>', methods = ['PUT'])
def epost(id):
    user = User.query.filter_by(fullname = request.authorization.get('username')).first()
    if(user and user.password == request.authorization.get('password')):
        content = Content.query.get(id)
        content.title = request.json['title']
        content.body = request.json['body']
        content.summary = request.json['summary']
        db.session.commit()
        return jsonify({"title": content.title, "body": content.body, "summary": content.summary})
    else:
        message = 'User credentials are incorrect'
        return jsonify({"message": message})
    
if __name__ == '__main__':
    app.run(debug = True)
