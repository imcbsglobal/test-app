# StockView API (Django REST)

This is the backend for a stock viewing app, built with Django and Django REST Framework.

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/stockview-api.git
cd stockview-api/backend
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv env
env/Scripts/activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework psycopg2-binary python-decouple
pip freeze > requirements.txt
```

### 4. Start the Project and App

```bash
django-admin startproject omega .
python manage.py startapp api
```

---

## 🔧 Environment Variables

Create a `.env` file in the `backend/` folder:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=your_host
DATABASE_PORT=5432
```

---

## 🏁 Running the Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## 📦 Updating Dependencies

Every time you add a new package, update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## 📁 Project Structure

```
omega-python/
│
├── backend/
│   ├── api/
│   ├── omega/
│   ├── env/
│   ├── requirements.txt
│   └── manage.py
├── README.md
```
