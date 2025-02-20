pip install flask flask-mysql flask-bcrypt flask-login



from flask import Flask, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change this if your MySQL user is different
app.config['MYSQL_PASSWORD'] = ''  # Add your MySQL password if applicable
app.config['MYSQL_DB'] = 'job_portal'  # Change this to your database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Class
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user['id'], user['username'])
    return None

# Sign Up Function
def register_user(username, email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        return "Email already registered."
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password))
    mysql.connection.commit()
    cur.close()
    return "Registration successful."

# Login Function
def login_user_auth(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    if user and bcrypt.check_password_hash(user['password'], password):
        user_obj = User(user['id'], user['username'])
        login_user(user_obj)
        return "Login successful."
    return "Invalid credentials."

# Logout Function
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
