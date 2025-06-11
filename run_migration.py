from app import app, db

with app.app_context():
    # Create all database tables
    db.create_all()
    print("Database tables created successfully.")

    # Add a test admin user if not exists
    from app import User
    from werkzeug.security import generate_password_hash
    
    if not User.query.filter_by(email='admin@speedycourier.com').first():
        admin = User(
            email='admin@speedycourier.com',
            password=generate_password_hash('admin123', method='sha256'),
            name='Admin User',
            phone='+1234567890',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created:")
        print("Email: admin@speedycourier.com")
        print("Password: admin123")
