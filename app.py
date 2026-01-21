from flask import request, session, jsonify
from sqlalchemy.exc import IntegrityError

from config import create_app, db
from models import User, UserSchema

app = create_app()

user_schema = UserSchema()

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


if __name__ == "__main__":
    app.run(port=5555, debug=True)

