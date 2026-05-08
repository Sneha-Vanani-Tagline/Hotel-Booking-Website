# Hotel Booking Website

A full-stack Hotel Booking Web Application built using Flask.  
This project allows users to search hotels, book rooms, manage bookings, and enables hosts/admins to manage hotel listings and rooms.


---

# Technologies Used

## Backend
- Python
- Flask
- Flask SQLAlchemy
- PostgreSQL

## Frontend
- HTML
- CSS
- JavaScript
- Bootstrap
- Jinja2 Templates

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Sneha-Vanani-Tagline/Hotel-Booking-Website.git
```

## Move to Project Folder

```bash
cd Hotel-Booking-Website
```

## Create Virtual Environment

```bash
python3 -m venv .venv
```

## Activate Virtual Environment

### Mac/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY = your_key
MAIL_USERNAME = your_gmail@gmail.com
MAIL_PASSWORD = your_email_app_password
SQLALCHEMY_DATABASE_URI = postgres_url
```

---

# Run Application

```bash
flask run
```

or

```bash
python run.py
```

---

# Database

This project uses PostgreSQL.

Example database URI:

```text
postgresql://username:password@localhost/demo_db
```

---

# Author

Sneha Vanani
