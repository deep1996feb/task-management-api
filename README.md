#  Task Management API

A scalable Task Management API built using Django REST Framework with JWT Authentication, Celery, Redis, and Django Signals.

---

##  Features

- User Registration & Login (JWT Authentication)
- Create, Read, Update, Delete Tasks
- Filter tasks by status
- Pagination support
- Mark task as completed
- Background processing using Celery & Redis
- Event-driven architecture using Django Signals
- Input validation and secure environment configuration

---

##  Tech Stack

- Python
- Django
- Django REST Framework
- MySQL 
- Celery
- Redis

---

##  Project Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/deep1996feb/task-management-api.git
cd task-management-api/task_manager

2️⃣ Create Virtual Environment

python -m venv env
env\Scripts\activate   # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Create .env File

SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

CELERY_BROKER_URL=redis://127.0.0.1:6379/0

5️⃣ Run Migrations

python manage.py makemigrations
python manage.py migrate

6️⃣ Run Server

python manage.py runserver

 Celery & Redis Setup
1️⃣ Run Redis (Docker)

docker run -d -p 6379:6379 redis

2️⃣ Start Celery Worker

python -m celery -A task_manager worker -l info --pool=solo

3️⃣ What Happens

When a task is created → Celery runs async job
Logs: "Task created successfully for user

Django Signals
Triggered when task status is updated to COMPLETED
Logs: "User completed a task"

API Endpoints

Authentication
Method	Endpoint	Description
POST	/api/register/	Register user
POST	/api/login/	Login user

Tasks
Method	Endpoint	Description
POST	/api/tasks/	Create task
GET	/api/tasks_list/	List tasks
GET	/api/tasks_detail/{id}/	Get single task
PUT	/api/tasks/{id}/update/	Full update
PATCH	/api/tasks/{id}/update/	Update status
DELETE	/api/tasks/{id}/delete/	Delete task

🔍 Filtering Example
/api/tasks_list/?status=PENDING

📌 Key Highlights
Clean architecture with separation of concerns
Async processing using Celery + Redis
Event-driven system using Django Signals
Secure environment variable handling
User-specific data access (security implemented)
