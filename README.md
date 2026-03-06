# CRICXO E-commerce

A Python-based e-commerce website with AI/ML features for the CRICXO brand.

## Features

- User authentication
- Product catalog with search
- Shopping cart
- Checkout with simulated payment
- Order management
- Admin panel
- AI-powered product recommendations
- Product reviews and ratings
- Bootstrap responsive design

## Setup (Development)

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Run server: `python manage.py runserver`

## Deployment to Heroku

1. **Install Heroku CLI** (if not installed): Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Static files & Whitenoise**
   - Add to `cricxo/settings.py`:
     ```python
     STATIC_ROOT = BASE_DIR / 'staticfiles'
     MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
     ```
   - Run `python manage.py collectstatic` before deploy (Heroku does this automatically).
   - Ensure `whitenoise` is in `requirements.txt` (installed above).

2. **Prepare for Production**:
   - Update `cricxo/settings.py` for production:
     ```python
     DEBUG = False
     ALLOWED_HOSTS = ['your-heroku-app.herokuapp.com']
     SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
     DATABASES = {
         'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
     }
     ```
   - Install `dj-database-url` and `psycopg2` for PostgreSQL:
     `pip install dj-database-url psycopg2-binary`
   - Update `requirements.txt`

3. **Create Heroku App**:
   - `heroku create your-app-name`
   - `heroku addons:create heroku-postgresql:hobby-dev`

4. **Deploy**:
   - `git init` (if not already)
   - `git add .`
   - `git commit -m "Initial commit"`
   - `git push heroku main`

5. **Configure Environment Variables**:
   - `heroku config:set SECRET_KEY=your-secret-key`
   - `heroku config:set STRIPE_PUBLIC_KEY=pk_live_...`
   - `heroku config:set STRIPE_SECRET_KEY=sk_live_...`

6. **Run Migrations on Heroku**:
   - `heroku run python manage.py migrate`
   - `heroku run python manage.py createsuperuser`

7. **Access Your Site**: `heroku open`

## Technologies

- Django
- Django REST Framework
- Bootstrap
- Scikit-learn
- Pandas
- NumPy
- Stripe (for payments)