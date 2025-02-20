from flask import Flask, render_template, jsonify
import pymysql

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

@app.route('/')
def home():
    """Render homepage with jobs from MySQL"""
    jobs = fetch_jobs()
    return render_template('home.html', jobs=jobs, company_name='Sumit')

@app.route('/api/jobs')
def list_jobs():
    """Return job listings as JSON from MySQL"""
    jobs = fetch_jobs()
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
