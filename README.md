# SpeedyCourier - Modern Logistics Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SpeedyCourier is a comprehensive logistics and shipment management system designed to streamline package tracking and delivery operations. The platform provides a seamless experience for both customers and administrators, offering real-time shipment tracking, status updates, and efficient delivery management.

## 🌟 Features

### For Customers
- User authentication and profile management
- Create and track shipments with real-time updates
- View detailed shipment history and status
- Receive email notifications for important updates

### For Administrators
- Dashboard with shipment statistics and analytics
- Manage shipments and update statuses
- View and manage all customer orders
- Generate reports and track delivery performance
- User management system

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.0.1**: Lightweight WSGI web application framework
- **Flask-SQLAlchemy**: SQL toolkit and ORM for database operations
- **Flask-Login**: User session management
- **Flask-Migrate**: Database migrations
- **Werkzeug**: Security and password hashing

### Frontend
- **HTML5 & CSS3**: Structure and styling
- **Bootstrap 5.1.3**: Responsive design framework
- **JavaScript**: Interactive elements and AJAX requests
- **Font Awesome 5.15.4**: Icons and visual elements

### Database
- **SQLite**: Development database (included)
- **PostgreSQL**: Production-ready database (recommended)

### Deployment
- **Gunicorn**: WSGI HTTP Server
- **Nginx**: Reverse proxy and load balancer
- **Docker**: Containerization (optional)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodeWithRonnie/Couriers.git
   cd Couriers
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///site.db
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-email-password
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   flask run
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 📂 Project Structure

```
Couriers/
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
├── README.md              # This file
├── instance/              # Instance folder
├── migrations/            # Database migrations
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/             # HTML templates
    ├── admin/             # Admin panel templates
    ├── auth/              # Authentication templates
    ├── errors/            # Error pages
    └── main/              # Main application templates
```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - your.email@example.com

Project Link: [https://github.com/CodeWithRonnie/Couriers](https://github.com/CodeWithRonnie/Couriers)

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
- [Font Awesome Icons](https://fontawesome.com/)
- [GitHub Emoji Cheat Sheet](https://www.webfx.com/tools/emoji-cheat-sheet/)