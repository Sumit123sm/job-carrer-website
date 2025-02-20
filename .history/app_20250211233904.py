from flask import Flask, render_template, jsonify,request, redirect, session    
import pymysql
import bcrypt

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',  # Change this if using a remote MySQL database
    'user': 'root',  # Your MySQL username
    'password': '',  # Your MySQL password
    'database': 'job_portal',  # Your database name
}

def get_db_connection():
    """Connect to MySQL database"""
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        return None

def fetch_jobs():
    """Fetch job listings from MySQL database"""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, location, salary FROM jobs")
            jobs = cursor.fetchall()
        return jobs
    finally:
        connection.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
            connection.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['email'] = user['email']
                return redirect('/')
            else:
                return "Invalid email or password!"

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                connection.commit()
            connection.close()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Log the user out"""
    session.clear()
    return redirect('/')


# @app.route('/')
# def home():
#     """Render homepage with jobs from MySQL"""
#     jobs = fetch_jobs()
#     return render_template('home.html', jobs=jobs, company_name='Sumit')
@app.route('/')
def hello_word():
  return render_template('home.html', jobs=jo, company_name='Sumit')

@app.route('/api/jobs')
def list_jobs():
    """Return job listings as JSON from MySQL"""
    jobs = fetch_jobs()
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
