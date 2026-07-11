from flask import Flask, render_template, request, jsonify
import mysql.connector
import re

app = Flask(__name__)

# Basic configuration parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Maria@2005', # Change this later to your actual MySQL password
    'database': 'crm_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

# Adding an alternative route array ensures Flask never 404s on this path
@app.route('/api/leads', methods=['POST'])
@app.route('/api/leads/', methods=['POST'])
def add_lead():
    # ... keep the rest of your function code exactly the same ...
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not message or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid input data"}), 400

    ai_summary = f"Client inquiry parsed. Length: {len(message)} characters."
    sentiment = "Positive" if any(w in message.lower() for w in ['good', 'great', 'help', 'need']) else "Neutral"

    # We will uncomment the database execution blocks once our MySQL server is running!
   # Connect and write data securely using prepared statements to prevent SQL injections
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO leads (name, email, message, ai_summary, sentiment) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, message, ai_summary, sentiment))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success", "message": "Pipeline validation clear!"}), 201

if __name__ == '__main__':
    app.run(debug=True)