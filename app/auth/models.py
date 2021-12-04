import datetime as dt
from hashlib import md5

from time import time

from flask import current_app
from flask_login import UserMixin
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.platform.models import Ad
from utils.database import Column, Model, SurrogatePK, db, relationship


user_role_table = db.Table(
    'user_role',
    Column('role_id', db.ForeignKey('roles.id'), primary_key=True),
    Column('user_id', db.ForeignKey('users.id'), primary_key=True)
)


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    users = relationship('User', secondary=user_role_table, back_populates='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = Column(db.String(30), nullable=False)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    last_seen = db.Column(db.DateTime, default=dt.datetime.utcnow)
    is_active = Column(db.Boolean(), default=False)
    is_blocked = Column(db.Boolean(), default=False)
    roles = relationship('Role', secondary=user_role_table, back_populates='users')
    ads = relationship('Ad', backref='user')

    def __init__(self, username, email, password, phone_number, **kwargs):
        db.Model.__init__(self, username=username, email=email, phone_number=phone_number, **kwargs)
        self.set_password(password)
        self.roles.append(Role.query.filter_by(name='user').first())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_jwt_token(self, expires_in=600):
        return jwt.encode(
            {
                'user_id': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_jwt_token(token):
        user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        return User.get_by_id(user_id)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
