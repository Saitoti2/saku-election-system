# 🗳️ SAKU Election System

<<<<<<< HEAD
Student's Association of KCA University - Election Management Platform

## 🚀 Quick Start (2 minutes)

### Option 1: Local Development
```bash
# Start the system locally
./start.sh
```

### Option 2: Minimal Setup
```bash
# Start minimal version
./start_minimal.sh
```

## 🌐 Access Your System

### Frontend (Student Portal)
- **URL**: http://localhost:5173
- **Features**: Student registration, document upload, personal portal

### Backend (Admin Dashboard)
- **URL**: http://localhost:8001
- **Features**: Admin dashboard, document verification, statistics

## 📱 Features

- ✅ **Student Registration** - Easy signup and profile management
- ✅ **Election Registration** - Council position registration
- ✅ **Document Verification** - Upload and verify required documents
- ✅ **Admin Dashboard** - Complete election management
- ✅ **WhatsApp Notifications** - Automated status updates
- ✅ **Mobile Responsive** - Works on all devices

## 🎯 For Your Presentation

1. **Start the system**: `./start.sh`
2. **Open browser**: http://localhost:5173
3. **Demo features**: Student portal, admin dashboard, mobile responsiveness
4. **Show auto-updates**: Push to GitHub = live updates

## 🔧 System Requirements

- Python 3.9+
- pip
- Modern web browser

## 🧱 Project Structure

- `saku-strategy/backend/` – **active Django backend** (`core` project). All API endpoints, admin dashboard, and deployment entrypoints live here.
- `saku-strategy/frontend/` – static student/admin portal served by `serve.py` during local demos.
- `docs/` – developer guides (see `docs/backend-overview.md` for backend workflows).
- `start.sh` – orchestrates the virtualenv, backend API, and static frontend for local demos (recommended).

> Tip: Always run backend commands (migrations, tests, shell) inside `saku-strategy/backend/` while the virtualenv from `./start.sh` is active.

## 📞 Support

For technical support or questions, contact the development team.
---
**Your SAKU Election System is ready for the KCA University student community!** 🎉
=======
A comprehensive Django-based election management system for KCA University's Student Association (SAKU) Council elections.

## 🚀 Features

### 👥 User Management
- **Student Registration** - Complete profile creation with academic details
- **Council Aspirant Registration** - Position-specific applications with document uploads
- **Delegate Management** - Department representative registration
- **Admin Dashboard** - Complete election management interface

### 📋 Document Management
- **Required Documents**:
  - School fees clearance (80%+)
  - Last 2 semester results (PDFs)
  - Current semester course registration
  - Certificate of good conduct
  - School ID image
  - Last 2 semester transcripts

### 🔐 Authentication & Security
- **JWT Authentication** - Secure token-based login
- **Role-based Access** - Student, Aspirant, Delegate, IECK, Admin roles
- **Document Validation** - File type and size validation
- **Secure File Uploads** - Organized document storage

### 📱 WhatsApp Integration
- **Verification Notifications** - Automatic status updates
- **Admin Alerts** - New registration notifications
- **Reminder System** - Incomplete application reminders
- **Dual Provider Support** - Meta Business API + Twilio fallback

### 🎨 Modern UI/UX
- **Responsive Design** - Works on all devices
- **Beautiful Interface** - Modern, professional design
- **Real-time Validation** - Instant form feedback
- **Progress Tracking** - Application status monitoring

## 🏗️ Technical Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL (Render's free tier)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **File Storage**: Local + Render static files
- **Deployment**: Render.com
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Notifications**: WhatsApp API + Twilio

## 🚀 Quick Deploy to Render

### 1. Fork/Clone Repository
```bash
git clone <your-repo-url>
cd SAKU-Election-System-Render
```

### 2. Deploy to Render
1. Go to [Render.com](https://render.com)
2. Create new **Web Service**
3. Connect your GitHub repository
4. Use these settings:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
./start.sh
```

### 3. Add PostgreSQL Database
1. Create new **PostgreSQL** database on Render
2. Copy the **External Database URL**
3. Add as environment variable: `DATABASE_URL`

### 4. Environment Variables
Add these in Render dashboard:

```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# WhatsApp Configuration (Optional)
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
ADMIN_PHONE_NUMBER=+254769582779

# Twilio Configuration (Optional)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### 5. Deploy! 🎉
Click **Deploy** and wait for the magic to happen!

## 🔑 Default Login

After deployment, access the admin panel:
- **URL**: `https://your-app.onrender.com/admin/`
- **Username**: `admin`
- **Password**: `admin123`

## 📱 Frontend Pages

- **Login**: `/login/`
- **Registration**: `/register/`
- **Admin Dashboard**: `/admin-dashboard/`
- **Student Portal**: `/portal/`
- **Verification**: `/verify/`
- **Signup Complete**: `/signup-complete/`

## 🔌 API Endpoints

- **Authentication**: `/api/auth/login/`, `/api/auth/register/`
- **User Profiles**: `/api/profiles/`
- **Academic Data**: `/api/faculties/`, `/api/departments/`, `/api/courses/`
- **Delegates**: `/api/delegates/`
- **Dashboard Stats**: `/api/dashboard/stats/`

## 🎯 Council Positions

- **Chair (President)**
- **Vice Chair**
- **Secretary General**
- **Finance Secretary**
- **Academic Secretary**
- **Sports Secretary**
- **Special Interests Secretary**

## 📊 User Types

- **STUDENT** - Regular student
- **ASPIRANT** - Council position candidate
- **DELEGATE** - Department representative
- **IECK** - Independent Electoral Commission of Kenya member
- **ADMIN** - System administrator

## 🔄 Workflow

1. **Student Registration** → Complete profile with documents
2. **Admin Review** → Verify documents and eligibility
3. **WhatsApp Notification** → Status update sent to student
4. **Election Process** → Qualified candidates proceed
5. **Results Management** → Track and manage election results

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone <repo-url>
cd SAKU-Election-System-Render

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Environment Variables (Local)
Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## 📞 Support

For technical support or questions:
- **Email**: admin@saku.ac.ke
- **WhatsApp**: +254769582779

## 📄 License

© 2024 SAKU - Student's Association of KCA University

---

**Built with ❤️ for KCA University Students**# Force deployment Wed Sep 17 01:37:34 EAT 2025
>>>>>>> 33ad9e5e2edb60aa24020e0c6b1ba9800aa868d5
