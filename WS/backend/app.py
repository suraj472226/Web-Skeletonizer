from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define a directory to save skeleton files
SAVE_DIR = 'saved_skeletons'

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)


# Database configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Dbms@1234'
MYSQL_DB = 'skeletonizer_db'

# Create database connection
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# User Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    userName = data.get('userName')
    email = data.get('email')
    password = data.get('password')

    if not userName or not email or not password:
        return jsonify({'message': 'All fields are required!'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (userName, email, password) VALUES (%s, %s, %s)",
                       (userName, email, password))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except mysql.connector.Error as err:
        return jsonify({'message': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# User Login Endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user from the database
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Simple password check (replace with your logic)
    if user and user['password'] == password:
        return jsonify({'user': user}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

# Skeletonizer Endpoint
@app.route('/skeletonize', methods=['POST'])
def skeletonize():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required."}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup(["script", "style", "img", "video", "audio"]):
            element.decompose()

        skeleton = str(soup.prettify())

        # Save the skeleton as a text file with the URL in the filename
        safe_url = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '-')
        filename = os.path.join(SAVE_DIR, f"{safe_url}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(skeleton)

        return jsonify({"skeleton": skeleton, "message": "Skeleton saved to file."}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


    
@app.route('/api/saved-skeletons', methods=['GET'])
def get_saved_skeletons():
    try:
        skeletons = []
        # List files in the saved_skeletons directory
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith('.txt'):
                # Extract the URL from the filename
                url = filename.replace('_', '/').replace('-','').replace('.txt', '')
                skeletons.append({"url": url, "filename": filename})

        return jsonify(skeletons), 200
    except Exception as err:
        return jsonify({'message': str(err)}), 500

@app.route('/api/skeletons/<filename>', methods=['GET'])
def get_skeleton_by_filename(filename):
    try:
        with open(os.path.join(SAVE_DIR, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            return jsonify({"skeleton": content}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404
    except Exception as err:
        return jsonify({'message': str(err)}), 500




if __name__ == '__main__':
    app.run(debug=True)
