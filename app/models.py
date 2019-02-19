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
    habits = db.relationship("Habit", backref="creator", lazy="dynamic")
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# TODO: Add email / user password reset functionality back in
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


class Habit(db.Model):
    """ Represents a single habit
    Attributes:
        id (int): Unique habit ID
        habit (str): Description/title of habit
        timestamp (date): Date habit was created
        user_id (int): Foreign Key to unique User ID
        weekly_goal (int): Number of times to complete habit / week
        is_active (bool): True if habit isn't currently active
        active_today (bool): True if habit needs to be completed today

    """

    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(70))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    weekly_goal = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    habit_history = db.relationship("HabitHistory", backref="parent", lazy="dynamic")
    active_today = db.Column(db.Boolean, default=True)

    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)

    def complete_habit(self, user_id):
        finished_at = datetime.utcnow()
        update_history = HabitHistory(timestamp=finished_at, habit_id=self.id)
        db.session.add(update_history)
        self.active_today = False

    def increase_streak(self, weekly_count):
        weekly_count += 1
        if weekly_count >= self.weekly_goal:
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak

        return weekly_count

    def decrease_streak(self, weekly_count):
        weekly_count -= 1

        if (weekly_count + 1) == self.weekly_goal:
            if self.current_streak >= 1:
                self.current_streak -= 1
            if (self.current_streak + 1) == self.longest_streak:
                if self.longest_streak >= 1:
                    self.longest_streak -= 1

        return weekly_count

    def reset_current_streak(self):
        self.current_streak = 0
        db.session.commit()

    def reset_longest_streak(self):
        self.longest_streak = 0
        db.session.commit()

    def __repr__(self):
        return "<Habit {}>".format(self.habit)


class HabitHistory(db.Model):
    """ Represents a log of each time a habit is completed
    Attributes:
        id (int): Unique log id
        timestamp (date): Date habit was completed
        habit_id (int): Foreign key to unique habit id
    """

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"))

    def __repr__(self):
        return "<{} Completed at {}".format(self.habit_id, self.timestamp)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
