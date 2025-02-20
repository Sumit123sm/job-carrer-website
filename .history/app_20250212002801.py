from flask import Flask, render_template, jsonify
import MySQLdb

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',  # Change this if your database is hosted elsewhere
    'user': 'root',  # Replace with your MySQL username
    'password': 'your_password',  # Replace with your MySQL password
    'database': 'job_portal',  # Replace with your database name
}

def get_db_connection():
    return MySQLdb.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        passwd=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        cursorclass=MySQLdb.cursors.DictCursor
    )

def fetch_jobs():
    """Fetch job listings from the database."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, location, salary FROM jobs")  # Ensure the 'jobs' table exists
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return jobs

@app.route('/')
def home():
    jobs = fetch_jobs()
    return render_template('home.html', jobs=jobs, company_name='Sumit')

@app.route('/api/jobs')
def list_jobs():
    jobs = fetch_jobs()
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
