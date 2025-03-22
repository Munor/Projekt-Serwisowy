from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja bazy danych SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja SQLAlchemy
db = SQLAlchemy(app)

# Import modelu po zainicjalizowaniu db
from models import ServiceRequest

@app.route('/')
def index():
    requests = ServiceRequest.query.all()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        is_business = 'business' in request.form
        device_type = request.form['device_type']
        manufacturer = request.form.get('manufacturer') if device_type == "Laptop" else None
        custom_manufacturer = request.form.get('custom_manufacturer') if manufacturer == "Inne" else None
        serial_number = request.form['serial_number']

        if is_business:
            new_request = ServiceRequest(
                business_name=request.form['business_name'],
                business_nip=request.form['business_nip'],
                business_person=request.form['business_person'],
                device_type=device_type,
                manufacturer=manufacturer if manufacturer != "Inne" else custom_manufacturer,
                custom_manufacturer=custom_manufacturer,
                serial_number=serial_number,
                description=request.form['description']
            )
        else:
            new_request = ServiceRequest(
                client_name=request.form['client_name'],
                client_surname=request.form['client_surname'],
                device_type=device_type,
                manufacturer=manufacturer if manufacturer != "Inne" else custom_manufacturer,
                custom_manufacturer=custom_manufacturer,
                serial_number=serial_number,
                description=request.form['description']
            )
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/release/<int:request_id>')
def release_request(request_id):
    req = ServiceRequest.query.get_or_404(request_id)
    req.release_device()
    db.session.commit()
    return redirect(url_for('index'))

# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)