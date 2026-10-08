# 🏋️ FitTracker

## 📌 Project Overview

**FitTracker** is a full-stack **Gym Management System** developed using **Python and Django**. It helps manage gym members, trainers, memberships, attendance, and other gym-related operations through a centralized web application.

## 🚀 Features

* 👤 Member management
* 🏋️ Trainer management
* 💳 Membership plan management
* 📅 Attendance management
* 🔐 User authentication
* 📝 Member registration
* ✏️ Add, update, and delete records
* 📊 Gym management dashboard
* 🛠️ Django admin panel
* 📱 User-friendly web interface

## 🛠️ Technologies Used

* **Python**
* **Django**
* **HTML5**
* **CSS3**
* **SQLite**
* **Git & GitHub**

## 📂 Project Structure

```text
FitTracker/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── gymapp/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   └── ...
│
└── static/
    ├── css/
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/adityaranjanswain01-tech/FitTracker.git
```

### 2. Navigate to the Project

```bash
cd FitTracker
```

### 3. Create a Virtual Environment

```bash
python -m venv gymenv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
gymenv\Scripts\activate
```

**Linux/macOS:**

```bash
source gymenv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

## 🔐 Admin Panel

The Django administration panel can be accessed at:

```text
http://127.0.0.1:8000/admin/
```

Use the superuser account created with:

```bash
python manage.py createsuperuser
```

## 🗄️ Database

FitTracker uses **SQLite** as its development database.

To create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📦 Requirements

All Python dependencies are stored in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

## 🔒 Git Ignore

The following files and folders should not be uploaded to GitHub:

```text
gymenv/
venv/
env/
__pycache__/
*.pyc
db.sqlite3
.env
.vscode/
.idea/
```
## 🔮 Future Improvements

* Online membership payments
* Workout and exercise tracking
* Diet and nutrition management
* Automated membership expiry notifications
* Email notifications
* Advanced attendance reports
* Analytics and performance dashboards
* Mobile application

## 👨‍💻 Author

**Jyotiraditya Ranjan Swain**

GitHub: [@adityaranjanswain01-tech](https://github.com/adityaranjanswain01-tech)
