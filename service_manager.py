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
    """Dodaje nowe zgłoszenie serwisowe.

    GET: Renderuje formularz dodawania zgłoszenia.
    POST: Przetwarza dane formularza, waliduje i zapisuje zgłoszenie do bazy.

    Returns:
        Response: Szablon add.html lub przekierowanie do strony głównej.
    """
    if request.method == 'POST':
        try:
            print(request.form)  # Debugowanie danych formularza
            is_business = 'business' in request.form
            device_type = request.form['device_type']
            manufacturer = request.form.get('manufacturer') if device_type == "Laptop" else None
            custom_manufacturer = request.form.get('custom_manufacturer') if manufacturer == "Inne" else None
            serial_number = request.form['serial_number']

            if ServiceRequest.query.filter_by(serial_number=serial_number).first():
                return render_template('add.html', error="Numer seryjny już istnieje!")

            if is_business:
                new_request = ServiceRequest(
                    business_name=request.form.get('business_name', ''),
                    business_nip=request.form.get('business_nip', ''),
                    business_person=request.form.get('business_person', ''),
                    device_type=device_type,
                    manufacturer=manufacturer if manufacturer != "Inne" else custom_manufacturer,
                    custom_manufacturer=custom_manufacturer,
                    serial_number=serial_number,
                    description=request.form['description']
                )
            else:
                new_request = ServiceRequest(
                    client_name=request.form.get('client_name', ''),
                    client_surname=request.form.get('client_surname', ''),
                    device_type=device_type,
                    manufacturer=manufacturer if manufacturer != "Inne" else custom_manufacturer,
                    custom_manufacturer=custom_manufacturer,
                    serial_number=serial_number,
                    description=request.form['description']
                )
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('add.html', error=f"Wystąpił błąd: {str(e)}")
    return render_template('add.html')

@app.route('/details/<int:request_id>')
def details_request(request_id):
    """Wyświetla szczegóły zgłoszenia serwisowego.

    Args:
        request_id (int): ID zgłoszenia.

    Returns:
        Response: Szablon details.html z danymi zgłoszenia lub 404.
    """
    req = ServiceRequest.query.get_or_404(request_id)
    return render_template('details.html', req=req)

@app.route('/release/<int:request_id>')
def release_request(request_id):
    """Oznacza zgłoszenie jako wydane.

    Args:
        request_id (int): ID zgłoszenia.

    Returns:
        Response: Przekierowanie do strony głównej.
    """
    req = ServiceRequest.query.get_or_404(request_id)
    req.release_device()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/generate_pdf/<int:id>')
def generate_pdf(id):
    """Generuje PDF dla zgłoszenia.

    Args:
        id (int): ID zgłoszenia.

    Returns:
        Response: Plik PDF jako załącznik.
    """
    req = ServiceRequest.query.get_or_404(id)
    html = render_template('pdf_template.html', req=req)
    pdf = pdfkit.from_string(html, False)
    return send_file(
        BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'zgłoszenie_{id}.pdf'
    )

@app.route('/')
def index():
    """Wyświetla listę zgłoszeń serwisowych.

    Returns:
        Response: Szablon index.html z listą zgłoszeń.
    """
    requests = ServiceRequest.query.order_by(ServiceRequest.date_received.desc()).all()
    return render_template('index.html', requests=requests)

# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)