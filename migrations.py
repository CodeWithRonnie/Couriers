from app import db
from datetime import datetime

# Create a new tracking event model
class TrackingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'location': self.location,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }

# Add relationship to Shipment model
class Shipment(db.Model):
    __tablename__ = 'shipment'  # Explicitly set table name to match existing table
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(20), unique=True, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_phone = db.Column(db.String(20), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    pickup_address = db.Column(db.String(200), nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Add relationship with tracking events
    tracking_events = db.relationship('TrackingEvent', backref='shipment', lazy=True, 
                                    order_by='desc(TrackingEvent.timestamp)')

# Run the migration
def upgrade():
    # Create the tracking_events table
    db.create_all()
    print("Database tables created/updated successfully.")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        upgrade()
