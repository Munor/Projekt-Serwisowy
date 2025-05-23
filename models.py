from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ServiceRequest(db.Model):
    """Model reprezentujący zgłoszenie serwisowe."""
    __tablename__ = 'requests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(100), nullable=True)
    client_surname = db.Column(db.String(100), nullable=True)
    business_name = db.Column(db.String(100), nullable=True)
    business_nip = db.Column(db.String(20), nullable=True)
    business_person = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=True)
    custom_manufacturer = db.Column(db.String(50), nullable=True)
    serial_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_received = db.Column(db.String(20), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_released = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default="W trakcie")

    def release_device(self):
        """Oznacza zgłoszenie jako wydane, ustawiając datę wydania i status."""
        self.date_released = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Wydany"