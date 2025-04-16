from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from models import ServiceRequest, db
from io import BytesIO
import pdfkit

app = Flask(__name__)

# Konfiguracja bazy danych SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja SQLAlchemy
db.init_app(app)

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

@app.route('/details/<int:id>')
def details(id):
    service_request = ServiceRequest.query.get_or_404(id)
    return render_template('details.html', service_request=service_request)

@app.route('/details/<int:id>/pdf')
def generate_pdf(id):
    service_request = ServiceRequest.query.get_or_404(id)
    html = render_template('pdf_template.html', service_request=service_request)
    pdf = pdfkit.from_string(html, False)
    return send_file(BytesIO(pdf), download_name=f'zgłoszenie_{id}.pdf', as_attachment=True)

@app.get('/release/<int:request_id>')
def release_request(request_id):
    req = ServiceRequest.query.get_or_404(request_id)
    req.release_device()
    db.session.commit()
    return redirect(url_for('index'))

@app.get('/')
def index():
    requests = ServiceRequest.query.all()
    return render_template('index.html', requests=requests)

# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)