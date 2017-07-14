# blogz
LC101 assignment

Web app using flask. Continuation of build-a-blog. 

## Entity Analysis

* A _blog_ is a series of _entries_
* Each _entry_ includes a title, body, and user

## Requirements

The app must meet several requirements:

* List all users on homepage 
* List all previous blog entries in reverse-chronological order
* Users must be _signed in_ before creating a new blog entry
* Users can log in 
* New users can register 
* Display the individual blog entry after creation
* Include a _menu bar_ with available commands

### Routes
* **"/"** - GET: Display list of all users 
* **"/blog"** - GET: Display list of all blog posts in reverse-chronological order 
* **"/blog?user=username"** - GET: Display blog entries for specific user 
* **"/blog/newpost"** - GET & POST: Display form for user to add new post 
* **"/login"** - GET & POST: Display form for user to log in 
* **"/signup"** - GET & POST: Display for for user to sign up 
