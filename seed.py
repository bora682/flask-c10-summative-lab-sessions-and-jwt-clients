from config import create_app, db
from models import User, Task

app = create_app()

with app.app_context():
    print("Seeding database...")

    # Clear existing data (safe for dev)
    Task.query.delete()
    User.query.delete()

    # Create a test user
    user = User(username="testuser")
    user.set_password("password123")

    db.session.add(user)
    db.session.commit()

    # Create a task for that user
    task = Task(
        title="Seeded Task",
        description="This task was created by seed.py",
        user_id=user.id
    )

    db.session.add(task)
    db.session.commit()

    print("Done seeding!")
