# CRICXO E-commerce

A modern Django e-commerce platform for the CRICXO brand with product catalog, cart, wishlist, reviews, and AI-powered recommendations.

## Features

- User authentication & profiles
- Product catalog with search functionality
- Shopping cart & checkout
- Simulated Stripe payment processing
- Order management
- Admin panel for product management
- AI-powered collaborative filtering recommendations
- Product reviews and ratings
- Wishlist functionality
- Bootstrap 5 responsive design

## Technologies

- Django 6.0.3
- Django REST Framework
- Bootstrap 5
- Scikit-learn & Pandas (ML recommendations)
- Stripe API
- PostgreSQL (production) / SQLite (development)
- Whitenoise (static file serving)

## Setup (Development)

1. Clone and install:
   ```bash
   git clone <your-repo-url>
   cd CRICXO.VS
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Start development server:
   ```bash
   python manage.py runserver
   ```
   Visit http://127.0.0.1:8000/ in your browser.

## Deployment to Heroku

### Prerequisites
- Heroku CLI installed
- Git repository initialized and pushed to GitHub
- Stripe API keys (test or live)

### Step-by-step

1. **Log in to Heroku:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create cricxo-store  # choose your own name
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Deploy code:**
   ```bash
   git push heroku main
   ```

4. **Configure environment variables:**
   ```bash
   heroku config:set SECRET_KEY='your-random-secret-key'
   heroku config:set DEBUG=False
   heroku config:set STRIPE_PUBLIC_KEY=pk_live_...
   heroku config:set STRIPE_SECRET_KEY=sk_live_...
   ```
   (Heroku automatically provides DATABASE_URL)

5. **Run migrations:**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku run python manage.py collectstatic
   ```

6. **Open your site:**
   ```bash
   heroku open
   ```
   Your app is now live! Visit `/admin/` to add products.

### Custom Domain

```bash
heroku domains:add www.yourdomain.com
```

Then update your domain's DNS settings (CNAME) to point to Heroku.

### Monitoring

```bash
heroku logs --tail
heroku config   # view env vars
```

## Local Testing Before Deploy

```bash
python manage.py collectstatic
python manage.py check --deploy
```

## Project Structure

```
CRICXO.VS/
├── cricxo/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/               # Main app
│   ├── models.py        # Product, Order, Review, Wishlist
│   ├── views.py         # Views & AI recommendations
│   ├── urls.py
│   └── templates/
├── static/              # CSS, JS, images
├── templates/           # Base templates
├── manage.py
├── Procfile             # Heroku configuration
├── runtime.txt          # Python version
└── requirements.txt     # Dependencies
```

## API Endpoints

- `GET /` – Product listing with search
- `GET /product/<id>/` – Product detail with reviews & recommendations
- `POST /product/<id>/add/` – Add to cart
- `GET /cart/` – View cart
- `POST /checkout/` – Process order
- `GET /wishlist/` – View wishlist
- `POST /wishlist/add/<id>/` – Add to wishlist
- `GET /profile/` – User profile & orders
- `/admin/` – Admin panel

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT License – see LICENSE file for details.
