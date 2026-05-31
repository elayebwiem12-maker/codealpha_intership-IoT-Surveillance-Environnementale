from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_readings(limit=20):
    """Récupérer les dernières lectures depuis SQLite."""
    conn = sqlite3.connect('sensor.db')
    rows = conn.execute(
        'SELECT timestamp, temperature, humidity FROM readings ORDER BY id DESC LIMIT ?',
        (limit,)
    ).fetchall()
    conn.close()
    return [{"timestamp": r[0], "temperature": r[1], "humidity": r[2]} for r in rows]

@app.route('/api/data')
def api_data():
    """Retourne les 20 dernières lectures."""
    data = get_readings(limit=20)
    return jsonify(data)

@app.route('/api/latest')
def api_latest():
    """Retourne la dernière lecture uniquement."""
    data = get_readings(limit=1)
    return jsonify(data[0] if data else {})

@app.route('/api/history')
def api_history():
    """Retourne les 24 dernières heures de données."""
    conn = sqlite3.connect('sensor.db')
    rows = conn.execute(
        """SELECT timestamp, temperature, humidity FROM readings
           WHERE timestamp >= datetime('now', '-24 hours')
           ORDER BY id DESC"""
    ).fetchall()
    conn.close()
    data = [{"timestamp": r[0], "temperature": r[1], "humidity": r[2]} for r in rows]
    return jsonify(data)

@app.route('/')
def home():
    return """
    <h2>API IoT Surveillance — CodeAlpha</h2>
    <ul>
        <li><a href='/api/data'>/api/data</a> — 20 dernières lectures</li>
        <li><a href='/api/latest'>/api/latest</a> — dernière lecture</li>
        <li><a href='/api/history'>/api/history</a> — historique 24h</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
