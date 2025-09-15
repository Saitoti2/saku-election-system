# SAKU Election System

A comprehensive election management system for SAKU (Saku University) built with Django REST Framework and modern web technologies.

## Features

- **Student Registration & Verification**: Document-based student verification system
- **Election Management**: Complete election lifecycle management
- **WhatsApp Integration**: Automated notifications via WhatsApp API
- **Admin Dashboard**: Comprehensive admin interface for election oversight
- **JWT Authentication**: Secure API authentication
- **Responsive Frontend**: Modern, mobile-friendly user interface

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework, JWT Authentication
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (development), PostgreSQL (production)
- **External APIs**: WhatsApp Business API, Twilio
- **Deployment**: Render.com

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saitoti2/saku-election-system.git
   cd saku-election-system
   ```

2. **Set up the backend**
   ```bash
   cd saku-strategy/backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   python serve.py
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Deployment on Render

This application is configured for easy deployment on Render.com:

### Environment Variables Required

```
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=core.settings
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
```

### Render Configuration

- **Build Command**: `cd saku-strategy/backend && pip install -r requirements.txt`
- **Start Command**: `cd saku-strategy/backend && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`

## Project Structure

```
saku-strategy/
├── backend/                 # Django backend
│   ├── core/               # Django project settings
│   ├── elections/          # Main election app
│   ├── scripts/            # Utility scripts
│   └── manage.py
└── frontend/               # Frontend HTML files
    ├── index.html          # Landing page
    ├── login-fixed.html    # Login page
    ├── admin-dashboard-enhanced.html
    └── ...                 # Other pages
```

## API Endpoints

- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `GET /api/elections/` - List elections
- `POST /api/elections/` - Create election
- `GET /api/students/` - List students
- `POST /api/students/verify/` - Verify student documents

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.