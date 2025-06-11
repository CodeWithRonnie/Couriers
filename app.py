from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

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
    weight = db.Column(db.Float)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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
        'description': shipment.description
    }
    
    return jsonify({
        'status': 'success',
        'data': shipment_data
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

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    else:
        shipments = Shipment.query.filter_by(user_id=current_user.id).order_by(Shipment.created_at.desc()).all()
    return render_template('dashboard.html', shipments=shipments)

@app.route('/create_shipment', methods=['GET', 'POST'])
@login_required
def create_shipment():
    if request.method == 'POST':
        # Handle shipment creation
        tracking_number = f"TRK{datetime.now().strftime('%Y%m%d%H%M%S')}"
        new_shipment = Shipment(
            tracking_number=tracking_number,
            sender_name=request.form.get('sender_name'),
            sender_phone=request.form.get('sender_phone'),
            receiver_name=request.form.get('receiver_name'),
            receiver_phone=request.form.get('receiver_phone'),
            pickup_address=request.form.get('pickup_address'),
            delivery_address=request.form.get('delivery_address'),
            weight=float(request.form.get('weight', 0)),
            description=request.form.get('description'),
            user_id=current_user.id
        )
        db.session.add(new_shipment)
        db.session.commit()
        
        flash(f'Shipment created successfully! Tracking number: {tracking_number}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_shipment.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
