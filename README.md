# Taskly 📝

Taskly is a Django-based task management app that supports user authentication, board and task management, and automated task reminders via Celery.

## 🚀 Features

- ✅ User registration and login (JWT-based)
- ✅ Boards and tasks creation
- ✅ Assign tasks to users
- ✅ Task reminders via email (Celery + Redis)
- ✅ REST API using Django REST Framework
- ✅ Tested with `pytest`

## 🧰 Tech Stack

- **Backend:** Django, Django REST Framework  
- **Asynchronous Tasks:** Celery  
- **Task Queue Broker:** Redis  
- **Database:** MySQL  
- **Testing:** Pytest  
- **Dev Tools:** pipenv, pre-commit, Docker (optional)

## 🧪 Local Development Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.9+
- MySQL
- Redis
- Docker & Docker Compose (optional)

### Setup Instructions

Clone the repo
```
git clone https://github.com/KaiG04/taskly.git
cd taskly
```

Set up virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies with pipenv
```
pip install pipenv
```
Install the project dependencies:
```
pipenv install --dev
```
Activate the pipenv shell:
```
pipenv shell
```
Set up configuration files
Copy example config files
```
cp dev.py.example dev.py
cp my.cnf.example my.cnf
```

Apply database migrations

Make sure your MySQL server is running, then apply the migrations to set up the database schema:
```
python manage.py migrate
```

# Start the Django development server
```
python manage.py runserver
```

# Run Redis using Docker:
```
docker run -p 6379:6379 redis
```

# Start Celery
```
celery -A taskly worker --loglevel=info
```

# Running Tests 
```
pytest
```


