# Flask Task Manager API

This project is a Flask backend API that implements session-based authentication and user-owned task management with full CRUD functionality and pagination.

---

## Features

- User signup, login, logout, and session validation
- Session-based authentication using cookies
- Protected routes
- Task CRUD operations (Create, Read, Update, Delete)
- Task ownership enforcement
- Pagination for task listing
- Database seeding script

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite

---

## Setup Instructions

1. CLone the repository:
```bash
git clone <your-repo-url>
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

2. Install dependencies:
```bash
pipenv install
pipenv shell
```

3. Run database migrations:
```bash
flask db upgrade
```

4. Seed the database:
```bash
python seed.py
```

5. Start the server:
```bash
flask run --port 5555
```

---

## Authorization 

All task routes require an authenticated session
Users may only access and modify their own tasks

---

## Notes

The SQLite database file is ignored via .gitignore