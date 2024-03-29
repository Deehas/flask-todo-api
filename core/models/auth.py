from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login
from flask_login import UserMixin
from ..models.todo import Todo


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # to get all todos assigned to the user
    todo = db.relationship("Todo", backref="author", lazy="dynamic")

    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
        return data

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
# Keeps user logged in
def load_user(id):
    return User.query.get(int(id))
