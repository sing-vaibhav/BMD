# 🎨 RangAura — Django Web Application

> A full-stack Django art marketplace connecting painters with art collectors.

---

## 🚀 Quick Start

### 1. Clone / Extract the project
```bash
cd rangaura
```

### 2. One-shot setup (recommended)
```bash
bash setup.sh
```
This will:
- Create a virtual environment
- Install all dependencies
- Run database migrations
- Seed demo painting data
- Prompt you to create a superuser
- Run the server

### 3. Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py makemigrations
python manage.py migrate

# Seed demo data
python manage.py seed_data

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### 4. Open in browser
- **Website**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
rangaura/
├── manage.py
├── requirements.txt
├── setup.sh
├── db.sqlite3                  ← created on first run
│
├── rangaura/                   ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                       ← Main app
│   ├── models.py               ← Painting + PaintingRequest models
│   ├── views.py                ← All page views
│   ├── urls.py                 ← URL routing
│   ├── forms.py                ← Auth + Request forms
│   ├── admin.py                ← Admin panel config
│   └── management/
│       └── commands/
│           └── seed_data.py    ← Demo data seeder
│
├── templates/
│   ├── base.html               ← Master layout (nav, messages, footer)
│   ├── core/
│   │   ├── home.html           ← Landing page
│   │   ├── gallery.html        ← Gallery with filters
│   │   ├── painting_detail.html
│   │   ├── request_painting.html
│   │   ├── request_success.html
│   │   ├── dashboard.html
│   │   └── request_detail.html
│   └── auth/
│       ├── login.html
│       └── register.html
│
├── static/
│   ├── css/
│   │   └── style.css           ← Full stylesheet
│   └── js/
│       └── main.js             ← Interactive JS
│
└── media/
    ├── paintings/              ← Gallery painting images
    └── requests/               ← Custom request reference images
```

---

## 🔑 Features

| Feature | Description |
|---|---|
| **User Registration** | Username, email, password with strength meter |
| **Login / Logout** | Session-based auth with styled forms |
| **Gallery** | Dynamic paintings from DB with style filters and search |
| **Aura Value System** | Unique 4-metric score per painting |
| **Painting Detail** | Full page with Aura bars, related paintings |
| **Custom Painting Requests** | Form with image upload, drag-and-drop |
| **User Dashboard** | View all your requests with status tracking |
| **Admin Panel** | Full management with image previews and status badges |
| **Responsive Design** | Works on mobile, tablet, and desktop |

---

## 🎨 Admin Panel

Login at `/admin/` with your superuser credentials.

From the admin you can:
- **Add / edit paintings** — set title, artist, style, price, Aura scores, image
- **View painting requests** — see uploaded reference images, update status, add notes
- **Manage users** — view all registered accounts

---

## 📝 URL Routes

| URL | View | Auth Required |
|---|---|---|
| `/` | Home / Landing | No |
| `/gallery/` | Full Gallery | No |
| `/gallery/<id>/` | Painting Detail | No |
| `/request-painting/` | Custom Painting Form | ✅ Yes |
| `/request-painting/success/` | Success Page | ✅ Yes |
| `/dashboard/` | User Dashboard | ✅ Yes |
| `/dashboard/request/<id>/` | Request Detail | ✅ Yes |
| `/register/` | Registration | No |
| `/login/` | Login | No |
| `/logout/` | Logout (POST) | No |
| `/admin/` | Django Admin | Superuser |

---

## ⚙️ Settings Overview

Key settings in `rangaura/settings.py`:

```python
# Database
DATABASES = {'default': {'ENGINE': 'sqlite3', 'NAME': 'db.sqlite3'}}

# Media uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
```

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite (easy to swap to PostgreSQL)
- **Frontend**: Pure HTML/CSS/JS (no React, no Webpack)
- **Fonts**: Google Fonts (Playfair Display, DM Sans, Cinzel)
- **Image uploads**: Pillow + Django FileField

---

*Built by RangAura — Karan Rana & Shubham Lawate | Maharashtra, India*
