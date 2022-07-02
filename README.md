# Distinctiveness and Complexity:

This is an online community library where people can share and download books. Guest users who are not logged in can search for the books that they want and download them. Users who are signed in can donate books for other people as well as edit and delete the books they have donated.

This final project is distinct from all of the previous projects because none of the previous projects let the users upload and download files. It has an additional feature that make it more complex than other projects is that when a book is updated, it will appear at the top of the list when displayed on a page. It is not a social network because it doesn't let any user like or comment on other users's uploads. It is also not an e-commerce app because it don't let the users sell or buy things. This app is simply a CRUD (Create, Read, Update, Delete) app to store and manage files.

# What’s contained in each file:

* The models.py file contains all of the models of this app. There are 3 models: User, Book and Time_obj.
* The urls.py file contains all the url paths of this app.
* The templates/library folder contains all the html pages.
* The views.py contains all the views of this app:
    + The 'login_view', 'logout_view' and 'register' let the users login, logout and register for an account.
    + The 'index' view shows the index page, it get all the books in this app ordered by the last time they are updated, from most to least recent, and render them in the index.html.
    + The 'donate' view lets the users donate books, it will render a form in the donate.html, and receive information from that form to create a book.
    + The 'search' view searchs for books base on the query a user type into the search form, and render all the related books in search.html.
    + The 'profile' view will display a page where a loggined user can see all the books they have donated. In this page, the user can edit or deleted those books.
    + The 'edit' view lets the users edit a book. It will render a form in the edit.html page, where the information of the book is pre-filled, then the user can edit the information of that book, and save it.
    + The 'book' view is an API, it will return the information of a book in Json.
    + The 'delete' view is an API, it will let a user delete a book they have donated, by clicking on the "Delete" button.

# How to run this application:

Navigate to the root directory, where manage.py is located, then run the following commands:

+ python manage.py makemigrations
+ python manage.py migrate
+ python manage.py runserver


# Any other additional information about this project: 

No additional information.