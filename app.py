from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import desc, func, or_
from functools import wraps
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logistics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

class TrackingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'location': self.location,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }

class Shipment(db.Model):
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
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship with tracking events
    tracking_events = db.relationship('TrackingEvent', backref='shipment', lazy=True, 
                                    order_by=desc(TrackingEvent.timestamp))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'))
    
    def to_dict(self):
        """Convert notification to dictionary for JSON responses"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
            'shipment_id': self.shipment_id,
            'time_ago': self.get_time_ago()
        }
        
    def get_time_ago(self):
        """Get human-readable time difference"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 30:
            return self.created_at.strftime('%b %d, %Y')
        elif diff.days > 1:
            return f"{diff.days} days ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to get tracking information
@app.route('/api/track/<tracking_number>', methods=['GET'])
def get_tracking(tracking_number):
    """API endpoint to get tracking information for a shipment"""
    if not tracking_number:
        return jsonify({
            'status': 'error',
            'message': 'Tracking number is required'
        }), 400
    
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    
    if not shipment:
        return jsonify({
            'status': 'not_found',
            'message': 'No shipment found with this tracking number'
        }), 404
    
    # Get tracking events
    tracking_events = [event.to_dict() for event in shipment.tracking_events]
    
    # Format the response
    shipment_data = {
        'tracking_number': shipment.tracking_number,
        'status': shipment.status,
        'sender': shipment.sender_name,
        'receiver': shipment.receiver_name,
        'pickup_address': shipment.pickup_address,
        'delivery_address': shipment.delivery_address,
        'created_at': shipment.created_at.isoformat(),
        'weight': shipment.weight,
        'description': shipment.description,
        'tracking_events': tracking_events
    }
    
    return jsonify({
        'status': 'success',
        'data': shipment_data
    })

@app.route('/api/track/<tracking_number>/events', methods=['GET'])
def get_tracking_events(tracking_number):
    """API endpoint to get tracking events for a shipment"""
    if not tracking_number:
        return jsonify({'error': 'Tracking number is required'}), 400
    
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404
    
    events = [event.to_dict() for event in shipment.tracking_events]
    return jsonify(events)

@app.route('/api/track/<tracking_number>/update', methods=['POST'])
@login_required
def update_tracking(tracking_number):
    """API endpoint to update shipment status and add tracking events"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404
    
    # Update shipment status
    shipment.status = data['status']
    
    # Create new tracking event
    event = TrackingEvent(
        shipment_id=shipment.id,
        status=data['status'],
        location=data.get('location', ''),
        description=data.get('description', '')
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Tracking updated successfully',
        'event': event.to_dict()
    })

# Track page route
@app.route('/track', methods=['GET'])
def track():
    """Render the tracking page"""
    tracking_number = request.args.get('tracking_number', '').strip()
    return render_template('track.html', tracking_number=tracking_number)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

def generate_tracking_number():
    """Generate a unique tracking number in format SCYYMMDDXXXXX"""
    date_str = datetime.utcnow().strftime('%y%m%d')
    random_str = ''.join(random.choices(string.digits, k=5))
    return f'SC{date_str}{random_str}'

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's shipments
    shipments = Shipment.query.filter_by(user_id=current_user.id).order_by(Shipment.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', shipments=shipments)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard with shipment statistics and recent activity"""
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    # Get statistics for the admin dashboard
    stats = {
        'total_shipments': Shipment.query.count(),
        'in_transit': Shipment.query.filter_by(status='In Transit').count(),
        'out_for_delivery': Shipment.query.filter_by(status='Out for Delivery').count(),
        'delivered': Shipment.query.filter_by(status='Delivered').count(),
        'pending': Shipment.query.filter_by(status='Processing').count(),
        'exceptions': Shipment.query.filter_by(status='Exception').count(),
    }
    
    # Get recent shipments
    recent_shipments = Shipment.query\
        .order_by(Shipment.updated_at.desc())\
        .limit(10)\
        .all()
    
    # Get recent tracking events
    recent_events = TrackingEvent.query\
        .order_by(TrackingEvent.timestamp.desc())\
        .limit(10)\
        .all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_shipments=recent_shipments,
                         recent_events=recent_events)

@app.route('/shipments/create', methods=['GET', 'POST'])
@login_required
def create_shipment():
    if request.method == 'POST':
        try:
            # Generate tracking number
            tracking_number = generate_tracking_number()
            
            # Create new shipment
            new_shipment = Shipment(
                tracking_number=tracking_number,
                sender_name=request.form.get('sender_name'),
                sender_phone=request.form.get('sender_phone'),
                receiver_name=request.form.get('receiver_name'),
                receiver_phone=request.form.get('receiver_phone'),
                pickup_address=request.form.get('pickup_address'),
                delivery_address=request.form.get('delivery_address'),
                weight=float(request.form.get('weight', 0)),
                description=request.form.get('description', ''),
                user_id=current_user.id,
                status='Processing'  # Initial status
            )
            
            # Add initial tracking event
            initial_event = TrackingEvent(
                shipment=new_shipment,
                status='Processing',
                location=request.form.get('pickup_address'),
                description='Shipment created and awaiting pickup'
            )
            
            db.session.add(new_shipment)
            db.session.add(initial_event)
            db.session.commit()
            
            flash(f'Shipment created successfully! Tracking Number: {tracking_number}', 'success')
            return redirect(url_for('track_shipment', tracking_number=tracking_number))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating shipment: {str(e)}')
            flash('Error creating shipment. Please try again.', 'danger')
    
    return render_template('create_shipment.html')

@app.route('/tracking/<tracking_number>')
@login_required
def track_shipment(tracking_number):
    """View details of a specific shipment"""
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first_or_404()
    
    # Check if the current user is the owner or an admin
    if not current_user.is_admin and shipment.user_id != current_user.id:
        flash('You do not have permission to view this shipment.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get tracking events in chronological order
    tracking_events = TrackingEvent.query.filter_by(shipment_id=shipment.id)\
        .order_by(TrackingEvent.timestamp.asc())\
        .all()
    
    return render_template('track.html', 
                         shipment=shipment, 
                         tracking_events=tracking_events,
                         current_status=shipment.status)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def send_shipment_notification(shipment, status, location, notes=None):
    """Send notification to customer about shipment status update"""
    try:
        subject = f"Shipment {shipment.tracking_number} - Status Update: {status}"
        
        # In a real app, you would use a proper email template and possibly a background task
        message = f"""
        Your shipment {shipment.tracking_number} status has been updated to: {status}
        
        Location: {location}
        
        """
        if notes:
            message += f"Notes: {notes}\n\n"
            
        message += "Thank you for using SpeedyCourier!"
        
        # Log the notification (in a real app, you would send an email/SMS here)
        current_app.logger.info(f"Notification sent for shipment {shipment.tracking_number}: {status}")
        
        # Create a notification record in the database
        notification = Notification(
            user_id=shipment.user_id,
            title=f"Shipment {status}",
            message=f"Your shipment {shipment.tracking_number} is now {status}",
            shipment_id=shipment.id
        )
        db.session.add(notification)
        db.session.commit()
        
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending notification: {str(e)}")
        return False

@app.route('/admin/shipments/<tracking_number>/update', methods=['GET', 'POST'])
@login_required
def update_shipment_status(tracking_number):
    """Update shipment status and add tracking event"""
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first_or_404()
    
    if request.method == 'POST':
        status = request.form.get('status')
        location = request.form.get('location')
        description = request.form.get('description')
        notify_customer = 'notify_customer' in request.form
        
        # Create tracking event
        event = TrackingEvent(
            shipment_id=shipment.id,
            status=status,
            location=location,
            description=description,
            user_id=current_user.id
        )
        
        # Update shipment status if changed
        if shipment.status != status:
            shipment.status = status
            shipment.updated_at = datetime.utcnow()
        
        db.session.add(event)
        db.session.commit()
        
        # Send notification to customer if requested
        if notify_customer:
            send_shipment_notification(
                shipment=shipment,
                status=status,
                location=location,
                notes=description
            )
        
        flash(f'Shipment status updated successfully!', 'success')
        return redirect(url_for('track_shipment', tracking_number=tracking_number))
    
    # Get all tracking events for this shipment
    tracking_events = TrackingEvent.query\
        .filter_by(shipment_id=shipment.id)\
        .order_by(TrackingEvent.timestamp.asc())\
        .all()
    
    # Get available status options
    status_options = [
        'Processing',
        'In Transit',
        'Out for Delivery',
        'Delivered',
        'Exception'
    ]
    
    return render_template('admin/update_shipment.html',
                         shipment=shipment,
                         tracking_events=tracking_events,
                         status_options=status_options)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
