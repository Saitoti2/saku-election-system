# 🗳️ SAKU Election System

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
- `saku_election/` – legacy Django scaffold kept for reference. It is **not** used by `start.sh` or any deployment pipelines.
- `start.sh` – orchestrates the virtualenv, backend API, and static frontend for local demos (recommended).
- `start_minimal.sh` – lightweight launcher if you only need the static portal.

> Tip: Always run backend commands (migrations, tests, shell) inside `saku-strategy/backend/` while the virtualenv from `./start.sh` is active.

For a deeper dive into modules, commands, and environments see `docs/backend-overview.md`.

## 📞 Support

For technical support or questions, contact the development team.

---
**Your SAKU Election System is ready for the KCA University student community!** 🎉