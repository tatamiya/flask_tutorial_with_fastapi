from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str


def get_user_by_name(db, username: str):
    for user_id, user_in_db in db.items():
        if username == user_in_db["username"]:
            user = User(user_id=user_id, **user_in_db)
            return user


def get_user_by_id(db, user_id: int):
    user_in_db = db.get(user_id)
    return User(user_id=user_id, **user_in_db)


def create_user(db, username: str, hashed_password: str):
    user_id = max(db.keys()) + 1
    db[user_id] = {
        "username": username,
        "hashed_password": hashed_password,
    }
    return user_id
