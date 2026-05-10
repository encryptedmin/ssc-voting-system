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
- `DATABASE_URL`: PostgreSQL connection string in production
- `CSRF_TRUSTED_ORIGINS`: comma-separated trusted origins, for example `https://your-app.onrender.com`
- `DJANGO_SUPERUSER_USERNAME`: optional deployment admin username
- `DJANGO_SUPERUSER_EMAIL`: optional deployment admin email
- `DJANGO_SUPERUSER_PASSWORD`: optional deployment admin password

## Render Deployment

This repo includes `render.yaml` and `build.sh`. The build command runs:

```bash
bash build.sh
```

Set `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` in Render before deploying if you want an admin account created automatically.

## Main Features

- Landing page for the e-election portal
- Voter registration and admin approval
- Admin dashboard with election CRUD and voter management
- Mobile-friendly ballot casting
- Live election count and participation charts
