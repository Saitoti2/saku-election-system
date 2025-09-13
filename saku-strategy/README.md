# SAKU Strategy App - KCA University Election Management

A data-driven delegate management and AI strategy platform for SAKU (Student's Association of KCA University) elections, built with Django + React.

## 🎯 Overview

This application helps political parties strategically organize delegates across all departments to ensure:
- **Constitutional Compliance**: All rules derived from SAKU Constitution with citations
- **Departmental Balance**: Minimum 3 delegates per department (configurable)
- **Gender Balance**: Configurable gender ratio requirements per department
- **Strategic Planning**: AI-powered what-if simulations and optimization
- **Real-time Monitoring**: Live dashboard with win score and risk alerts

## 🏗️ Architecture

```
saku-strategy/
├── backend/                 # Django + DRF + Analytics
│   ├── elections/          # Core models (Department, Course, Delegate)
│   ├── rules_engine/       # Constitution-based rule validation
│   ├── analytics/          # Features, simulator, optimizer
│   └── parsers/            # PDF parsing (Constitution + Departments)
├── frontend/               # React + TypeScript + Vite
├── rules/                  # rules.yaml (auto-generated from Constitution)
├── data/                   # departments.csv (parsed from PDF)
├── reports/                # Constitution extracts
└── uploads/                # Source documents
```

## 🚀 Quick Start

### Option 1: One-Command Start (Recommended)
```bash
cd saku-strategy
./start.sh
```
This will automatically:
- Set up the backend with virtual environment
- Install dependencies
- Run migrations
- Seed sample data
- Start both backend and frontend servers

### Option 2: Docker
```bash
cd saku-strategy
docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

### Option 3: Manual Setup
```bash
# Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Frontend (requires Node.js)
cd frontend
npm install
npm run dev
```

### Access Points
- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin (admin/admin123)

## 📊 Features

### 1. Document Parsing
- **Constitution Parser**: Extracts eligibility rules, gender balance, representation requirements
- **Departments Parser**: Extracts department structure and courses
- **Auto-generates**: `rules/rules.yaml` with constitutional citations

### 2. Delegate Management
- **CRUD Operations**: Create, read, update, delete delegates
- **Eligibility Validation**: Automatic rule checking on creation
- **Vetting Pipeline**: Track delegate vetting status
- **Bulk Import**: CSV import/export capabilities

### 3. Analytics & Strategy
- **Win Score**: Composite score (0-100) based on coverage and balance
- **What-If Simulator**: Test scenarios before implementing
- **Risk Assessment**: Identify under-covered departments
- **Optimization**: Suggest minimal actions to meet targets

### 4. Real-time Dashboard
- **Department Tiles**: Progress toward targets
- **Gender Balance**: Visual representation per department
- **Risk Alerts**: Highlight compliance issues
- **Score Tracking**: Live win score updates

## 🔧 Configuration

### Rules Configuration (`rules/rules.yaml`)
```yaml
min_per_department:
  value: 3
  scope: "department"
  citation: "Article III, Sec 2(b)"
  editable: true

gender_balance:
  metric: "ratio"
  target: { female_min: 0.33 }
  tolerance: 0.05
  scope: "department"
  citation: "Article IV, Sec 1(c)"
  editable: true

eligibility:
  year_min: { value: 2, citation: "..." }
  gpa_min: { value: 2.5, citation: "..." }
  disciplinary_clear: { value: true, citation: "..." }
```

### Environment Variables
```bash
# backend/.env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
```

## 📡 API Endpoints

### Core Resources
- `GET /api/departments/` - List all departments
- `GET /api/courses/` - List all courses
- `GET /api/delegates/` - List all delegates
- `POST /api/delegates/` - Create new delegate

### Analytics
- `GET /api/delegates/metrics/` - Department coverage metrics + win score
- `GET /api/delegates/risks/` - Risk assessment per department
- `POST /api/delegates/simulate/` - What-if simulation

### Example Simulation Request
```json
POST /api/delegates/simulate/
{
  "actions": [
    {
      "department": "ict",
      "add_candidates": 2,
      "gender": "Female"
    },
    {
      "department": "business",
      "convert_to_qualified": 1
    }
  ]
}
```

## 🧮 Win Score Algorithm

The win score (0-100) is calculated as:
```
score = 100
- w_min_gap * sum(gap_to_min_d)
- w_gender_gap * sum(gender_gap_d)
+ w_buffer * sum(max(0, qualified_d - target_min_d))
```

Where:
- `gap_to_min_d`: Shortfall below minimum delegates per department
- `gender_gap_d`: Deviation from target gender ratio
- `w_*`: Configurable weights in `rules.yaml`

## 📋 Usage Workflow

### 1. Initial Setup
1. Upload Constitution and Departments PDFs to `uploads/`
2. Run parsing: `python scripts/ingest_documents.py`
3. Review generated `rules/rules.yaml`
4. Adjust thresholds as needed

### 2. Delegate Recruitment
1. Add delegates via API or admin interface
2. System automatically validates eligibility
3. Track vetting progress
4. Monitor dashboard for coverage gaps

### 3. Strategic Planning
1. Use what-if simulator to test scenarios
2. Review risk assessment for problem areas
3. Use optimizer for action recommendations
4. Implement high-impact changes

### 4. Election Day
1. Export final delegate list
2. Monitor real-time metrics
3. Adjust strategy based on live data

## 🧪 Testing

```bash
# Backend tests
cd backend
source .venv/bin/activate
python manage.py test

# Frontend tests (if available)
cd frontend
npm test
```

## 📁 Project Structure Details

### Backend (`backend/`)
- **Django 4.2 LTS** with Django REST Framework
- **SQLite** for development, PostgreSQL for production
- **Modular apps**: elections, rules_engine, analytics
- **Constitution parsing** with PDF extraction
- **Rule validation** with constitutional citations

### Frontend (`frontend/`)
- **React 18** with TypeScript
- **Vite** for fast development
- **Axios** for API communication
- **Responsive design** with system fonts

### Data Flow
1. **PDFs** → **Parsers** → **rules.yaml + departments.csv**
2. **Rules** → **Validator** → **Delegate eligibility**
3. **Delegates** → **Analytics** → **Win score + risks**
4. **Simulations** → **Optimizer** → **Action recommendations**

## 🔒 Security & Compliance

- **Constitutional Compliance**: All rules traceable to specific clauses
- **Audit Trail**: Rule changes logged with citations
- **Role-based Access**: Admin, FieldOp, Viewer permissions
- **Data Validation**: Input sanitization and type checking

## 🚀 Deployment

### Production Checklist
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure PostgreSQL database
- [ ] Set secure `DJANGO_SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL certificates
- [ ] Configure static file serving
- [ ] Set up monitoring and logging

### Docker Production
```bash
docker compose -f docker-compose.prod.yml up -d
```

## 📈 Monitoring

### Key Metrics
- **Win Score**: Overall strategy effectiveness
- **Department Coverage**: Delegates per department
- **Gender Balance**: Ratio compliance per department
- **Vetting Pipeline**: Progress through qualification process

### Alerts
- Departments below minimum threshold
- Gender balance violations
- Eligibility rule failures
- System errors or warnings

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📄 License

This project is for educational and strategic planning purposes for KCA University SAKU elections.

## 🆘 Support

For issues or questions:
1. Check the documentation
2. Review `ASSUMPTIONS.md` for configuration details
3. Check logs in `reports/` for parsing results
4. Verify `rules/rules.yaml` configuration

---

**Built with ❤️ for KCA University SAKU Elections**