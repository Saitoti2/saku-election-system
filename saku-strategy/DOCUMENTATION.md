# SAKU Strategy App - Complete Documentation

## 🎯 Project Overview

The SAKU Strategy App is a comprehensive data management and strategic planning tool designed to help political parties win KCA University SAKU (Student's Association of KCA University) committee elections. The application provides real-time analytics, delegate management, simulation capabilities, and strategic optimization tools.

## 🏗️ Architecture

### Technology Stack

**Backend:**
- **Django 4.2 LTS** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Python 3.9** - Runtime environment

**Frontend:**
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **React Query** - Data fetching and caching
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **Lucide React** - Icon library

**Additional Tools:**
- **Docker** - Containerization
- **NVM** - Node.js version management
- **Pytest** - Backend testing
- **ESLint** - Code linting

## 📁 Project Structure

```
saku-strategy/
├── backend/                    # Django backend
│   ├── core/                  # Django project settings
│   ├── elections/             # Main app for delegate management
│   ├── rules_engine/          # Constitutional rules processing
│   ├── analytics/             # AI/ML analytics and optimization
│   ├── parsers/               # Document parsing utilities
│   ├── scripts/               # Management scripts
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── manage.py             # Django management script
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Main application pages
│   │   ├── services/         # API service layer
│   │   ├── App.tsx           # Main application component
│   │   └── main.tsx          # Application entry point
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Vite configuration
├── rules/                     # Configuration files
│   └── rules.yaml            # Election rules and constraints
├── data/                     # Data files
│   └── departments.csv       # Department and course data
├── reports/                  # Generated reports
│   └── constitution_extract.md
├── uploads/                  # User uploaded files
├── docker-compose.yml        # Docker orchestration
├── Makefile                  # Development commands
└── README.md                 # Quick start guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (managed via NVM)
- Git

### Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   cd "SAKU ASSOCIATION STRATEGY APP/saku-strategy"
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python scripts/seed_sample_data.py
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   npm install
   ```

4. **Start the application:**
   ```bash
   # Terminal 1 - Backend
   cd backend && source .venv/bin/activate && python manage.py runserver 0.0.0.0:8000
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

5. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api
   - Django Admin: http://localhost:8000/admin (admin/admin123)

## 🎛️ Features

### 1. Dashboard
- **Real-time Metrics**: Win score, qualified delegates, department status
- **Visual Analytics**: Interactive charts and graphs
- **Status Monitoring**: Department compliance and gender balance tracking
- **Auto-refresh**: Configurable data updates

### 2. Delegate Management
- **CRUD Operations**: Create, read, update, delete delegates
- **Advanced Filtering**: Search by name, department, status
- **Bulk Operations**: Mass updates and imports
- **Status Tracking**: Vetting progress and qualification status

### 3. Strategy Simulator
- **What-if Analysis**: Test different scenarios
- **Impact Assessment**: Measure strategy changes
- **Auto-optimization**: AI-powered strategy recommendations
- **Real-time Updates**: Instant feedback on changes

### 4. Reports & Analytics
- **Multiple Report Types**: Overview, delegates, departments, gender balance
- **Export Capabilities**: PDF and CSV generation
- **Visual Reports**: Charts and graphs
- **Customizable Views**: Filter and sort data

### 5. Settings & Configuration
- **Election Rules**: Configurable parameters
- **System Preferences**: Auto-refresh, notifications
- **Advanced Settings**: API endpoints, database status

## 🔧 API Endpoints

### Delegates
- `GET /api/delegates/` - List all delegates
- `POST /api/delegates/` - Create new delegate
- `GET /api/delegates/{id}/` - Get specific delegate
- `PATCH /api/delegates/{id}/` - Update delegate
- `DELETE /api/delegates/{id}/` - Delete delegate

### Analytics
- `GET /api/delegates/metrics/` - Get comprehensive metrics
- `GET /api/delegates/risks/` - Get risk analysis
- `POST /api/delegates/simulate/` - Run simulation
- `POST /api/delegates/optimize/` - Run optimization

### Departments & Courses
- `GET /api/departments/` - List departments
- `GET /api/courses/` - List courses

## 🧪 Testing

### Backend Tests
```bash
cd backend
source .venv/bin/activate
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

### Individual Services
```bash
# Backend
cd backend
docker build -t saku-backend .
docker run -p 8000:8000 saku-backend

# Frontend
cd frontend
docker build -t saku-frontend .
docker run -p 5173:5173 saku-frontend
```

## 📊 Data Models

### Core Models

**Department**
- `code`: Unique identifier
- `name`: Department name

**Course**
- `department`: Foreign key to Department
- `name`: Course name

**Delegate**
- `full_name`: Delegate's full name
- `gender`: Gender (Male/Female/Other)
- `department`: Foreign key to Department
- `course`: Foreign key to Course
- `year_of_study`: Academic year
- `student_id`: Unique student identifier
- `contacts`: JSON field for contact information
- `vetting_status`: NOT_STARTED/IN_PROGRESS/PASSED/FAILED
- `is_qualified`: Boolean qualification status
- `notes`: Additional notes

## 🔒 Security Features

- **CORS Configuration**: Secure cross-origin requests
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Prevention**: React's built-in protections
- **Environment Variables**: Secure configuration management

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   pkill -f "python manage.py runserver"
   pkill -f "npm run dev"
   ```

2. **Node.js Not Found**
   ```bash
   export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   nvm use 18
   ```

3. **Python Virtual Environment Issues**
   ```bash
   cd backend
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Database Migration Issues**
   ```bash
   cd backend
   source .venv/bin/activate
   python manage.py makemigrations
   python manage.py migrate
   ```

## 📈 Performance Optimization

- **React Query Caching**: Intelligent data caching
- **Lazy Loading**: Component-based code splitting
- **Database Indexing**: Optimized database queries
- **CDN Ready**: Static asset optimization
- **Compression**: Gzip compression enabled

## 🔮 Future Enhancements

- **Real-time Notifications**: WebSocket integration
- **Mobile App**: React Native version
- **Advanced Analytics**: Machine learning predictions
- **Multi-tenant Support**: Multiple election support
- **API Rate Limiting**: Enhanced security
- **Audit Logging**: Comprehensive activity tracking

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review the API documentation
- Examine the test cases for usage examples
- Check the console logs for error details

## 📄 License

This project is proprietary software developed for KCA University SAKU elections.

---

**Last Updated**: September 2025
**Version**: 1.0.0
**Status**: Production Ready

