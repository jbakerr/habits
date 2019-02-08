from datetime import datetime, date, timedelta
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
from app import db, login


class User(UserMixin, db.Model):
    """ Represents a single user
    Attributes:
        id (int): Unique user ID
        email (str): Unique user email
        password_hash (str): Hashed user password
        last_seen (date): UTC date of last login

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    habbits = db.relationship('Habbit', backref='creator', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def get_reset_password_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'reset_password': self.id, 'exp': time() + expires_in},
    #         current_app.config['SECRET_KEY'],
    #         algorithm='HS256').decode('utf-8')

    # @staticmethod
    # def verify_reset_password_token(token):
    #     try:
    #         id = jwt.decode(token, current_app.config['SECRET_KEY'],
    #                         algorithms=['HS256'])['reset_password']
    #     except:
    #         return
    #     return User.query.get(id)


class Habbit(db.Model):
    """ Represents a single habbit
    Attributes:
        id (int): Unique habbit ID
        habbit (str): Description/title of habbit
        timestamp (date): Date habbit was created
        user_id (int): Foreign Key to unique User ID
        weekly_goal (int): Number of times to complete habbit / week
        is_active (bool): True if habbit isn't currently active

    """
    id = db.Column(db.Integer, primary_key = True)
    habbit = db.Column(db.String(70))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weekly_goal = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    habbit_history = db.relationship('HabbitHistory', backref='parent', lazy='dynamic')

    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)

    # habbit_history = db.relationship('HabbitHistory', backref='history', lazy='dynamic')

    # @classmethod
    # def create_habbit(cls, habbit, user_id, weekly_goal):
    #     habit = cls.create(habbit=habbit, user_id=user_id, weekly_goal=weekly_goal)
    #     habbit_summary = HabbitSummary(habbit_id = habbt.id)
    #     db.session.add(habbit)
    #     db.session.add(habbit_summary)
    #     db.session.commit()

    def complete_habbit(self, user_id):
        finished_at = datetime.utcnow()
        update_history = HabbitHistory(timestamp=finished_at, habbit_id = self.id)
        db.session.add(update_history)

    def update_streak(self, habbit_history):
        yesterday = date.today() - timedelta(1)
        last_record = habbit_history[-1].timestamp.date()
        if last_record < yesterday:
            self.current_streak = 1
        else:
            self.current_streak += 1
            if self.current_streak >= self.longest_streak:
                self.longest_streak = self.current_streak
        return ""


    def __repr__(self):
        return '<Habbit {}>'.format(self.habbit)

class HabbitHistory(db.Model):
    """ Represents a log of each time a habbit is completed
    Attributes:
        id (int): Unique log id
        timestamp (date): Date habbit was completed
        habbit_id (int): Foreign key to unique habbit id
        user_id (int): Foreign Key to unique User ID
    """
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    habbit_id = db.Column(db.Integer, db.ForeignKey('habbit.id'))



    def __repr__(self):
        return '<{} Completed at {}'.format(self.habbit_id, self.timestamp)




@login.user_loader
def load_user(id):
    return User.query.get(int(id))
