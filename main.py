from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:pizza@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 'sunflowerseeds'

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
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

#Creates email and password properties for User class. 
    def __init__(self, email, password):
        self.email = email
        self.password = password

#user is allowed to visit /login or /register if they are not logged on. If user wants to access a different site and are not logged in, then redirect them to login page ..
@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

#create /newpost route and renders add template. If user leaves title or body blank, then return errors. 
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(email=session['email']).first()

        if title == "":
            flash("Please fill in the title", "error")

        if body == "":
            flash("Please fill in the body", "error")
            
        if len(title) > 1 and len(body) > 1:   
            new_post = Blog(title, body, owner) #'owner', not 'owner_id" or 'user' since 'owner' is property of Blog class
            db.session.add(new_post)
            db.session.commit()
            blog_id = str(new_post.id) #grab the id for the record you just created
            return redirect('/blog?id='+blog_id)
        else: 
            return render_template('newpost.html', title=title, body=body)
        
    return render_template('newpost.html')

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
            flash("Logged in",'info')
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
        existing_user = User.query.filter_by(email=email).first()

        if email == "" or len(email) < 3:
            flash("Please provide a valid email", "error")

        if password == "" or len(password) < 3:
            flash("Please provide a valid password. Password must be between 3-20 charcters", "error")
        
        if password != verify or verify =="":
            flash("Passwords do not match", "error")

        if existing_user:
            flash("Duplicate username", 'error')

        if len(email) > 3 and len(password) > 3 and password==verify and not existing_user: 
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return render_template('signup.html', email=email)

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    flash('logged out','info')
    return redirect('/')


@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()