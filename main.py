from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:pizza@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#create a Blog class with id, title, body, and owner_id columns. 'owner_id' creates a column that references the 'user id' from User table. The use a a foregin key links the two tables. 
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#Creates title, body, and owner properties for Blog class. 
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

#create a User class with id, username, password, and blogs columns. 'blogs' links to Blogs table. 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

#Creates email and password properties for User class. 
    def __init__(self, email, password):
        self.email = email
        self.password = password


#create /newpost route and renders add template. If user leaves title or body blank, then return errors. 
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(email=session['email']).first()
        
        title_error = ""
        body_error = ""

        if title == "": 
            title_error = "Please fill in the title"
            body = ""

        if body == "":
            body_error = "Please fill in the body"
            title = ""
            
        if not title_error and not body_error:   
            new_post = Blog(title, body, owner) #'owner', not 'owner_id" or 'user' since 'owner' is property of Blog class
            db.session.add(new_post)
            db.session.commit()
            blog_id = str(new_post.id) #grab the id for the record you just created
            return redirect('/blog?id='+blog_id)
        else: 
            return render_template('add.html', title_error=title_error, body_error=body_error, title=title, body=body)
        
    return render_template('add.html')

#create /blog route to display blog
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #since this is a get request, use request.args.get to retrieve id of blog post
    blog_id = request.args.get('id')

    #if blog_id exists, send your db a query and find the post associated with that id. Render post.html with that post's title and blog
    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body)
    
# If there are no specific posts, show entire blog. 
    titles = Blog.query.all()
    return render_template('blog.html',titles=titles)

@app.route('/login', methods=['POST', 'GET'])
def login():
    # if post, means that user is trying to login and you need to verify email, password, and if user exists in database
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email    
            flash("Logged in")
            return redirect('/newpost')
        if user and not user.password:
            flash('User password incorrect', 'error')
            return redirect('/login')
        if not user:
            flash('User does not exist', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()