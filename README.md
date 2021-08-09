# cms 

Flask Api Assignment for content management system

This system will contain User and Content

The User have to register by entering data in fields such as fullname, email, password, phone, address, city, state, country, pincode.
All the fields are not mandatory

The Content will have fields such as title, body, summary, categories and pdf

Lines 1- 10: Importing required modules and setting database

Lines 12-57: 3 tables (User, Content, Categories)

Lines 59-76: (/addcategories/<int:id>) To add categories for a particular content based on id of content

Lines 78-91: (getcategories/<int:id>) To get all the categories for a particular content

Lines 94-125: (/addUser) Adding user and validating the user details

Lines 128-159: (/search1/<string:text>) Searching for text in the Content

Line 161-179: (/getUser) Get all the users registered

Line 181-235: (/getPost/<int:id>) Get the content for a particular user using id

Line 238-265: (/delemployee/<string:testingusername>/<int:id>) Deleting the content based on the username and id of the content

Line 259-282: (/getcontentforuser/<int:id>) Getting the content for a specified user id

Line 284-305: (/addcontent) Adding the content of a user

Line 308-330: (/editpost/<string:testingusername>/<int:id>): Editing the content for a user based on id

