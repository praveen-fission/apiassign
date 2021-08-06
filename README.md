# apiassign

Flask Api Assignment for content management system

This system will contain User and Content

The User have to register by entering data in fields such as fullname, email, password, phone, address, city, state, country, pincode.
All the fields are not mandatory

The Content will have fields such as title, body, summary, categories and pdf

Lines 42-73: (/addUser) Adding user and validating the user details

Lines 76-107: (/search1/<string:text>) Searching for text in the Content

Line 109-127: (/getUser) Get all the users registered

Line 129-182: (/getPost/<int:id>) Get the content for a particular user using id

Line 185-212: (/delemployee/<string:testingusername>/<int:id>) Deleting the content based on the username and id of the content

Line 216-229: (/getcontentforuser/<int:id>) Getting the content for a specified user id

Line 236-255: (/addcontent) Adding the content of a user

Line 258-280: (/editpost/<string:testingusername>/<int:id>): Editing the content for a user based on id

