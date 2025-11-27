from flask import Flask, Response, request
import sqlite3
import random
from prometheus_client import Gauge, Counter, generate_latest

app = Flask(__name__)

# --- Prometheus metric'leri ---
random_number_metric = Gauge("random_number", "Random number between 1-100")
counter_metric = Counter("counter_total", "Total number of /metrics calls")

# --- /metrics endpoint ---
@app.route("/metrics")
def metrics():
    counter_metric.inc()
    random_number_metric.set(random.randint(1, 100))

    output = generate_latest()

    return Response(
        output,
        mimetype="text/plain; version=0.0.4; charset=utf-8"
    )

# --- / endpoint ---
@app.route("/")
def home():
    conn = sqlite3.connect("/data/demo.db")
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
    msg = request.args.get("msg")
    if not msg:
        return "Please provide a message, e.g. /add?msg=Hello"

    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (message) VALUES (?)", (msg,))
    conn.commit()
    conn.close()

    return f"Record added successfully: '{msg}'"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
