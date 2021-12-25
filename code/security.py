from user import User

from werkzeug.security import safe_str_cmp

users = [
    User(1, 'bob', 'asdf'),
]

username_mapping = {u.username: u for u in users}
userid_maping = {u.id: u for u in users}


def authenticate(username, password):
    user = userid_maping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_maping.get(user_id, None)
