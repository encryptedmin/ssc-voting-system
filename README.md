# SSC Voting System

A Django-based e-election system for Colegio de Kidapawan Supreme Student Council elections.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Environment Variables

- `SECRET_KEY`: Django secret key for production
- `DEBUG`: set to `False` in production
- `ALLOWED_HOSTS`: comma-separated hosts for deployment, for example `your-app.onrender.com`

## Main Features

- Landing page for the e-election portal
- Voter registration and admin approval
- Admin dashboard with election CRUD and voter management
- Mobile-friendly ballot casting
- Live election count and participation charts
