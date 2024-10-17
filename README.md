# Inventory Management API

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL or MySQL database
4. Configure Redis
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Endpoints

- POST /items/
- GET /items/{id}/
- PUT /items/{id}/
- DELETE /items/{id}/

## Authentication

- POST /token/ (JWT login)
