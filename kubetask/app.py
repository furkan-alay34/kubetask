from flask import Flask, jsonify, request
import sqlite3
import random

app = Flask(__name__)
counter = 0

# --- /metrics endpoint ---
@app.route("/metrics")
def metrics():
    global counter
    counter += 1
    data = {
        "random_number": random.randint(1, 100),
        "counter": counter
    }
    return jsonify(data)

# --- / endpoint ---
@app.route("/")
def home():
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO records (message) VALUES (?)", ("First record!",))
        conn.commit()

    cursor.execute("SELECT message FROM records ORDER BY id DESC LIMIT 1")
    last_record = cursor.fetchone()
    conn.close()

    if last_record:
        return f"Hello from Demo-App! Last record: {last_record[0]}"
    else:
        return "Hello from Demo-App! No records found."

# --- /add endpoint ---
@app.route("/add")
def add_record():
    msg = request.args.get("msg")  # URL'deki ?msg= parametresini alır
    if not msg:
        return "Please provide a message, e.g. /add?msg=Hello"

    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (message) VALUES (?)", (msg,))
    conn.commit()
    conn.close()

    return f"Record added successfully: '{msg}'"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
