# blogz
LC101 assignment

Web app using flask. Continuation of build-a-blog. 

## Entity Analysis

* A _blog_ is a series of _entries_
* Each _entry_ includes a title, body, and user

## Requirements

The app must meet several requirements:

* List all _users_ on homepage 
* List all _previous blog entries_ in reverse-chronological order
* Users must be _signed in_ before creating a new blog entry
* Users can _log in_
* New users can _register_ 
* Display the _individual blog entry_ after creation
* Include a _menu bar_ with available commands

## User Scenarios
* User enters a username that is stored in the database with the correct password and is redirected to the /newpost page with their username being stored in a session
* User enters a username that is stored in the database with an incorrect password and is redirected to the /login page with a message that their password is incorrect
* User tries to login with a username that is not stored in the database and is redirected to the /login page with a message that this username does not exist 

## Routes
* **"/"** - GET: Display list of all users 
* **"/blog"** - GET: Display list of all blog posts in reverse-chronological order 
* **"/blog?user=username"** - GET: Display blog entries for specific user 
* **"/blog/newpost"** - GET & POST: Display form for user to add new post 
* **"/login"** - GET & POST: Display form for user to log in 
* **"/signup"** - GET & POST: Display for for user to sign up 
