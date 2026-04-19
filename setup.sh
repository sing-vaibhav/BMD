#!/bin/bash
# ═══════════════════════════════════════════════════
#  RangAura — One-Shot Setup Script
#  Run: bash setup.sh
# ═══════════════════════════════════════════════════

set -e
echo ""
echo "🎨 Setting up RangAura Django Project..."
echo "═══════════════════════════════════════════"

# 1. Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# 3. Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# 4. Seed demo data
echo ""
echo "🌱 Seeding demo paintings..."
python manage.py seed_data

# 5. Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true

# 6. Create superuser prompt
echo ""
echo "═══════════════════════════════════════════"
echo "👤 Create Admin Superuser"
echo "═══════════════════════════════════════════"
python manage.py createsuperuser

echo ""
echo "═══════════════════════════════════════════"
echo "✅ RangAura is ready!"
echo ""
echo "▶  Run the server:   python manage.py runserver"
echo "🌐  Open:            http://127.0.0.1:8000"
echo "🔑  Admin Panel:     http://127.0.0.1:8000/admin/"
echo "═══════════════════════════════════════════"
