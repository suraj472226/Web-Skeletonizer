from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dbms@1234'
app.config['MYSQL_DB'] = 'skeletonizer_db'

# Initialize MySQL
from flask_mysqldb import MySQL
mysql = MySQL(app)

# Home Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Web Skeletonizer API!'}), 200

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()

    if account:
        return jsonify({'message': 'Account already exists!'}), 409
    else:
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'You have successfully registered!'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Your logic to check email and password
    if email != 'example@example.com' or password != 'password123':  # Replace with your validation
        return jsonify({'message': 'Invalid email or password'}), 401

    # Successful login response
    return jsonify({'message': 'Login successful'}), 200

# User Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully!'}), 200

# Generate Skeleton
@app.route('/skeletonize', methods=['POST'])
def skeletonize():
    if not session.get('loggedin'):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'message': 'URL is required'}), 400

    # Validate URL
    if not re.match(r'^(http|https)://', url):
        url = 'http://' + url

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Strip scripts, styles, images, and multimedia
        for element in soup(['script', 'style', 'img', 'video', 'audio']):
            element.decompose()

        skeleton_html = soup.prettify()

        # Save skeleton to database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO skeletons (user_id, url, skeleton_html) VALUES (%s, %s, %s)',
            (session['id'], url, skeleton_html)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'skeleton': skeleton_html}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get User's Saved Skeletons
@app.route('/skeletons', methods=['GET'])
def get_skeletons():
    if not session.get('loggedin'):
        return jsonify({'message': 'Unauthorized'}), 401

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, url, skeleton_html FROM skeletons WHERE user_id = %s', (session['id'],))
    skeletons = cursor.fetchall()
    cursor.close()

    return jsonify(skeletons), 200

# Delete a Skeleton
@app.route('/skeletons/<int:id>', methods=['DELETE'])
def delete_skeleton(id):
    if not session.get('loggedin'):
        return jsonify({'message': 'Unauthorized'}), 401

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM skeletons WHERE id = %s AND user_id = %s', (id, session['id']))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Skeleton deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
