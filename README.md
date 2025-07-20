# ✈️ ALX Travel App - Backend (0x00)
This repository (`alx_travel_app_0x00`) is a duplicate of the `alx_travel_app project`, specifically for the 0x00 task focusing on Django database modeling, serializers, and data seeding.

## Project Objective
The primary objective of this project is to set up the foundational backend components for a travel application, including:
- Defining robust database models for core entities like `Listing`, `Booking`, and `Review`.
- Creating Django REST Framework serializers to facilitate API interactions for `Listing` and `Booking` data.
- Implementing a Django management command to efficiently populate the database with sample data for development and testing purposes.
---
## Directory Structure
```
alx_travel_app_0x00/
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── listings/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       │   └── __init__.py
│       ├── models.py             # Database models for Listing, Booking, Review
│       ├── serializers.py        # DRF serializers for API data representation
│       ├── tests.py
│       └── views.py
│       └── management/
│           └── commands/
│               └── __init__.py
│               └── seed.py       # Management command to seed the database
├── manage.py
└── README.md                   # This file
```
---
## Project Setup
Setup and Installation
Follow these steps to set up and run the project:

1. Clone the repository (or ensure you have the duplicated project):
```
# git clone https://github.com/your-username/alx_travel_app.git alx_travel_app_0x00
# cd alx_travel_app_0x00
```
Make sure you are in the `alx_travel_app_0x00` directory.

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Django and Django REST Framework:
```bash
pip install Django djangorestframework Faker django-environ mysqlclient
```
> Note: `Faker` is required for the seeding command, `django-environ` for environment variables, and `mysqlclient` for MySQL database connection.

4. Configure .env file:
Create a `.env` file in the `alx_travel_app_0x00/alx_travel_app/` directory (where `manage.py` is located) and add your `SECRET_KEY` and `DATABASE_URL`.
Refer to the `dotenv-example` immersive for content.

**Example `.env` content**:
```
SECRET_KEY=your_very_long_and_random_secret_key_here_for_security
DEBUG=True
DATABASE_URL=mysql://<your_mysql_user>:<your_mysql_password>@127.0.0.1:3306/<your_mysql_database_name>
```
**Remember to replace placeholders with your actual values.**

5. Configure settings.py:
Ensure `listings`, `rest_framework`, `corsheaders`, `drf_yasg`, and `django_filters` are added to your `INSTALLED_APPS` in `alx_travel_app_0x00/alx_travel_app/settings.py`. Also, ensure `django-environ` is correctly used to read `SECRET_KEY` and `DATABASE_URL`.

6. Run Database Migrations:
This will create the tables for your `Listing`, `Booking`, and `Review` models in your database.
```bash
python manage.py makemigrations listings
python manage.py migrate
```
---
## Running the Seeder Command
After setting up the database, you can populate it with sample data using the custom management command:
```bash
python manage.py seed --num_listings 20 --clear_existing
```
- `--num_listings`: (Optional) Specify the number of listings to create (default is 10).
- `--clear_existing`: (Optional) Use this flag to delete all existing `Listing`, `Booking`, and `Review` data before seeding new data. Use with caution in production environments.
---
## Verification
After running the seeder, you can verify the data by:
- **Accessing the Django Admin**: Create a superuser (`python manage.py createsuperuser`) and log in to the admin interface (`http://127.0.0.1:8000/admin/`). You should see your `Listing`, `Booking`, and `Review` models populated with data.
- **Inspecting the database directly**: Use a database client to query the `listings_listing`, `listings_booking`, and `listings_review` tables.
---
### Author
- [Ahmed Kamal  - GitHub Profile](https://github.com/ahmedkamal313)