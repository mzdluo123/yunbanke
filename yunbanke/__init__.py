from .user import User
import json


def save_session(user: User, file: str):
    with open(file, "w") as file:
        data = json.dumps(user.dump_token(), sort_keys=True, indent=4, separators=(',', ':'))
        file.write(data)


def load_session(file: str) -> User:
    user = User()
    with open(file, "r") as file:
        data = json.loads(file.read())
        user.restore_token(data)
    return user