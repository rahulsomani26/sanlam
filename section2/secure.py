from user import User
users = [
    User(1, 'rahul', 'rahul@123'),
    User(2, 'ujjwal', 'ujju_12')
]

# create a username mapping

username_mapping = {u.username: u for u in users}  # dictionary comprehension


# create a userid mapping
userid_mapping = {u.id: u for u in users}  # dictionary comprehension


def authenticate(username, password):
    user = username_mapping.get(username, 'Access not granted')
    if user and user.password == password:
        return user


def identity(payload):
    # This contains the content of the JSON web token
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
