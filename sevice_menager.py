from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT NOT NULL,
                    device TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date_received TEXT NOT NULL,
                    date_released TEXT,
                    status TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

class ServiceRequest:
    def __init__(self, client_name, device, description, request_id=None, date_received=None, date_released=None, status="W trakcie"):
        self.client_name = client_name
        self.device = device
        self.description = description
        self.request_id = request_id
        self.date_received = date_received or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_released = date_released
        self.status = status

    def release_device(self):
        self.date_released = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Wydany"

class ServiceManager:
    def __init__(self):
        init_db() 

    def add_request(self, client_name, device, description):
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        date_received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO requests (client_name, device, description, date_received, status) VALUES (?, ?, ?, ?, ?)",
                  (client_name, device, description, date_received, "W trakcie"))
        conn.commit()
        request_id = c.lastrowid
        conn.close()
        return request_id

    def release_request(self, request_id):
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("UPDATE requests SET date_released = ?, status = ? WHERE request_id = ?",
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Wydany", request_id))
        affected_rows = c.rowcount
        conn.commit()
        conn.close()
        return affected_rows > 0

    def get_requests(self):
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("SELECT request_id, client_name, device, description, date_received, date_released, status FROM requests")
        rows = c.fetchall()
        conn.close()
        return [ServiceRequest(row[1], row[2], row[3], row[0], row[4], row[5], row[6]) for row in rows]

manager = ServiceManager()

@app.route('/')
def index():
    requests = manager.get_requests()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        client_name = request.form['client_name']
        device = request.form['device']
        description = request.form['description']
        manager.add_request(client_name, device, description)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/release/<int:request_id>')
def release_request(request_id):
    manager.release_request(request_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)