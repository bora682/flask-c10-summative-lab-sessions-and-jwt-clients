from flask import request, session, jsonify
from sqlalchemy.exc import IntegrityError

from config import create_app, db
from models import User, UserSchema, Task, TaskSchema


app = create_app()

user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# --------------------
# AUTH ROUTES
# --------------------

@app.post("/signup")
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if password != password_confirmation:
        return {"errors": ["Passwords must match"]}, 422

    try:
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return user_schema.dump(user), 201

    except IntegrityError:
        db.session.rollback()
        return {"errors": ["Username already taken"]}, 422

    except ValueError as e:
        db.session.rollback()
        return {"errors": [str(e)]}, 422


@app.post("/login")
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter(User.username == username).first()

    if user and user.authenticate(password):
        session["user_id"] = user.id
        return user_schema.dump(user), 200

    return {"errors": ["Invalid username or password"]}, 401


@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
        if user:
            return user_schema.dump(user), 200

    return {"errors": ["Unauthorized"]}, 401


@app.delete("/logout")
def logout():
    session.pop("user_id", None)
    return {}, 204


# --------------------
# TASK ROUTES
# --------------------

@app.get("/tasks")
def get_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return {"errors": ["Unauthorized"]}, 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = Task.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "tasks": tasks_schema.dump(pagination.items),
        "page": page,
        "pages": pagination.pages,
        "total": pagination.total
    }, 200


@app.post("/tasks")
def create_task():
    user_id = session.get("user_id")

    if not user_id:
        return {"errors": ["Unauthorized"]}, 401

    data = request.get_json()

    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task_schema.dump(task), 201


@app.patch("/tasks/<int:id>")
def update_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return {"errors": ["Unauthorized"]}, 401

    task = Task.query.get(id)

    if not task or task.user_id != user_id:
        return {"errors": ["Not found"]}, 404

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)

    db.session.commit()

    return task_schema.dump(task), 200


@app.delete("/tasks/<int:id>")
def delete_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return {"errors": ["Unauthorized"]}, 401

    task = Task.query.get(id)

    if not task or task.user_id != user_id:
        return {"errors": ["Not found"]}, 404

    db.session.delete(task)
    db.session.commit()

    return {}, 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)

