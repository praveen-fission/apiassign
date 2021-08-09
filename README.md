# cms 

Flask Api Assignment for content management system

This system will contain User and Content

The User have to register by entering data in fields such as fullname, email, password, phone, address, city, state, country, pincode.
All the fields are not mandatory

The Content will have fields such as title, body, summary, categories and pdf


GET Request

1. Get all posts based on ID:  localhost:5000/getPost/2

2. Get content of a user:  localhost:5000/getcontentforuser/2

3. Search the text:  localhost:5000/search1/2nd body

4. Get all the categories of an id:  localhost:5000/getcategories/2


POST Request

1. Adding contents :  localhost:5000/addcontent

2. Adding user :  localhost:5000/addUser

3. Adding categories of an id:  localhost:5000/addcategories/1


PUT Request

1. Editing content :  localhost:5000/editpost/lily/29


DELETE Request

1. Deleting content based on ID :  localhost:5000/delemployee/marshal/5


User Schema
{
"email":"email",
"password":"password",
"fullname":"fullname",
"address":"address",
"city":"city",
"state":"state",
"country":"country",
"phone":"phone",
"pincode":"pincode"
}


Content Schema
{
"title":"title",
"body":"body",
"summary":"summary",
"tags":"tags",
"file":"file"
}


Categories Schema
{
"cat1": "cat1",
"cat2": "cat2",
"cat3": "cat3"
}
