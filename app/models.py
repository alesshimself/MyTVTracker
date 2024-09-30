import json

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login, milvus_collection


class User(UserMixin):
    def __init__(self, username, email, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        results = milvus_collection.query(f"id == {user_id}", output_fields=["user_data"])
        if results:
            user_data = json.loads(results[0]['user_data'])
            user = User(user_data['username'], user_data['email'], id=user_id)
            user.password_hash = user_data['password_hash']
            return user
        return None


@login.user_loader
def load_user(id):
    return User.get(int(id))


class TVShow:
    def __init__(self, tmdb_id, title, embedding):
        self.tmdb_id = tmdb_id
        self.title = title
        self.embedding = embedding


class Episode:
    def __init__(self, tmdb_id, show_id, season_number, episode_number):
        self.tmdb_id = tmdb_id
        self.show_id = show_id
        self.season_number = season_number
        self.episode_number = episode_number
        self.watched = False
