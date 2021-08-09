from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import re

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
    category = db.relationship('Content', backref = "categories", lazy = True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}', '{self.pincode}')"

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


class Content(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    body = db.Column(db.String(300), nullable = False)
    summary = db.Column(db.String(60), nullable = False)
    tags = db.Column(db.String(100))
    file = db.Column(db.BLOB())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    relate = db.relationship('Categories', backref = "category", lazy = True)

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

@app.route('/addcategories/<int:id>', methods = ['POST'])
def addcategories(id):
    content = Content.query.filter_by(id = id).first()
    # if(content and user.password == request.authorization.get('password')):
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

@app.route('/getcategories/<int:id>', methods = ['GET'])
def getcategories(id):
    cont = Content.query.filter_by(id = id).first()
    print(cont.relate)
    outer = []
    for cont in cont.relate:
        d={}
        d["cat1"] = cont.cat1
        d["cat2"]=cont.cat2
        d["cat3"]=cont.cat3
        # d["summary"] = cont.summary
        # d["phone"] = user.phone
        outer.append(d)
    return jsonify(outer)


@app.route('/addUser', methods = ['POST'])
def addUser():
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


@app.route('/search1/<string:text>', methods = ['GET', 'POST'])
def search1(text):
    data = Content.query.filter(Content.title.contains(text)).all()
    print(data)
    if(data):
        outer = []
        for dat in data:
            d = {}
            d['title'] = dat.title
            outer.append(d)
        return jsonify(outer)
    # elif(len(data) == 0):
    data = Content.query.filter(Content.body.contains(text)).all()
    print(data)
    if(data):
        outer = []
        for dat in data:
            d = {}
            d['body'] = dat.body
            outer.append(d)
        return jsonify(outer)
    # elif(len(data) == 0):
    data = Content.query.filter(Content.summary.contains(text)).all()
    print(data)
    if(data):
        outer = []
        for dat in data:
            d = {}
            d['summary'] = dat.summary
            outer.append(d)
        return jsonify(outer)
    return jsonify(data)

@app.route('/getUser', methods = ['GET'])
def getUser():
    users = User.query.all()

    outer = []
    for user in users:
        d={}
        d["id"] = user.id
        d["fullname"]=user.fullname
        d["email"]=user.email
        d["password"] = user.password
        d["phone"] = user.phone
        d["address"] = user.address
        d["city"] = user.city
        d["state"] = user.state
        d["country"] = user.country
        d["pincode"] = user.pincode
        outer.append(d)
    return jsonify(outer)

@app.route('/getPost/<int:id>', methods = ['GET'])
def getPost(id):
    # user = User.query.filter_by(fullname = 'marshal').first()
    # user1 = User.query.filter_by(fullname = 'lily').first()
    users = User.query.all()
    user1 = User.query.filter_by(id = id).first()
    # user1 = User.query.filter_by(testingusername == users[0].fullname).first()
    # print(user1)
    
    # print(users[3].id)
    # print(len(users))

    list_of_ids = []
    for i in range(len(users)):
        list_of_ids.append(users[i].id)
    print(list_of_ids)

    
    if(id in list_of_ids):
        print(f'id {id} is in database')

        outer = []
        print(len(user1.category))
        if(len(user1.category) == 0):
            error1 = 'there are no content for this user. Please add some content'
            return jsonify({"details":error1})
        else:
            # return redirect(url_for('login', id = id))
            for cont in user1.category:
                d={}
                d["id"] = cont.id
                d["title"]=cont.title
                d["body"]=cont.body
                d["summary"] = cont.summary
                d["tags"] = cont.tags
                # d["phone"] = user.phone
                outer.append(d)
            return jsonify(outer)
            return redirect('/login')
        # return render_template('loginform.html')
    else:
        error = 'id is not registered in our database'
        return jsonify({"error": error})
        # print('id is not registered in our database')
 
    outer = []
    for cont in user1.category:
        d={}
        d["id"] = cont.id
        d["title"]=cont.title
        d["body"]=cont.body
        d["summary"] = cont.summary
        # d["phone"] = user.phone
        outer.append(d)
    return jsonify(outer)


@app.route('/delemployee/<string:testingusername>/<int:id>',methods = ['DELETE'])
def delemployee(testingusername,id):
    user1 = User.query.filter_by(fullname = testingusername).first()
    print(user1)
    print(user1.pincode)
    print(user1.id)
    
    list_of_ids = []
    for con in user1.category:
        list_of_ids.append(con.id)
    print('end of for loop')
        
    outer = []
    for i,j in enumerate(list_of_ids):
        if(id in list_of_ids and id == j):
            cont = user1.category[i]
            print(cont)
            d = {}
            d["id"] = cont.id
            d["title"]=cont.title
            d["body"]=cont.body
            d["summary"] = cont.summary
            db.session.delete(cont)
            db.session.commit()
            outer.append(d)
            return jsonify(outer)

    return 'id is not present'


# to get content for a particular user
@app.route('/getcontentforuser/<int:id>', methods = ['GET'])
def getcontentforuser(id):
    # user = User.query.filter_by(fullname = request.authorization.get('username')).first()
    # if(user and user.password == request.authorization.get('password')):
    user1 = User.query.filter_by(id = id).first()
    outer = []
    for user in user1.category:
        d={}
        d["title"] = user.title
        d["body"] = user.body
        d["summary"] = user.summary
        d['tags'] = user.tags
        outer.append(d)
    return jsonify(outer)

@app.route('/addcontent', methods = ['POST'])
def addcontent():
    user = User.query.filter_by(fullname = request.authorization.get('username')).first()
    if(user and user.password == request.authorization.get('password')):
        print(user.fullname, user.password)
        title = request.form["title"]
        body = request.form["body"]
        summary = request.form["summary"]
        tags = request.form["tags"]
        pdf = request.files['pdf']
        abcd = pdf.read()
        print(title,body,summary,tags,pdf, abcd)

        cont  = Content(title = title, body = body, summary = summary, tags = json.dumps(tags), file = abcd ,user_id = user.id)

        db.session.add(cont)
        db.session.commit()
        return jsonify({"title":title, "body":body, "summary":summary, "tags": tags})
    else:
        # print(user.fullname, user.password)
        print(user)
        return jsonify({"error": "try again"})


@app.route('/editpost/<string:testingusername>/<int:id>', methods = ['PUT'])
def editpost(testingusername,id):
    user1 = User.query.filter_by(fullname = testingusername).first()

    list_of_ids = []
    for con in user1.category:
        list_of_ids.append(con.id)


    outer = []
    for i,j in enumerate(list_of_ids):
        if(id in list_of_ids and id == j):
            cont = user1.category[i]
            print(cont)
            cont.title = request.json['title']
            cont.body = request.json['body']
            cont.summary = request.json['summary']
            db.session.commit()

            return jsonify({"title": cont.title, "body": cont.body, "summary": cont.summary})


    return 'id is not present' 

if __name__ == '__main__':
    app.run(debug = True)
