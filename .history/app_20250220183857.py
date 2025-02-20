from flask import Flask, render_template, jsonify
import pymysql.cursors 
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',  # Change this if your database is hosted elsewhere
    'user': 'root',  # Replace with your MySQL username
    'password': os.getenv("pass"),  # Replace with your MySQL password
    'database': os.getenv("db"),  # Replace with your database name
}

def get_db_connection():
    """Establish a connection to MySQL database"""
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
    """Fetch job listings from the database."""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, location, salary FROM jobs")  # Ensure the 'jobs' table exists
            jobs = cursor.fetchall()
        return jobs
    finally:
        connection.close()

@app.route('/')
def home():
    jobs = fetch_jobs()
    return render_template('home.html', jobs=jobs, company_name='Jobs')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/courses.html')
def courses():
    return render_template('courses.html')
@app.route('/jobs.html')
def jobs():
    return render_template('jobs.html')
@app.route('/faq.html')
def faq():
    return render_template('faq.html')

@app.route('/api/jobs')
def list_jobs():
    jobs = fetch_jobs()
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True)
