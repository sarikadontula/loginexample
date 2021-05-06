from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'login'
app.config['MONGO_URI'] = 'mongodb+srv://sarika:dontula95151@cluster0.xjppw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST' , 'GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode("utf-8"), login_user['password'].encode("utf-8")) == login_user['password'].encode("utf-8"):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode("utf-8"), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

    
if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'redis'

    sess.init_app(app)

    app.debug = True
    app.run()