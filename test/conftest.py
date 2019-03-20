from app import create_app, db
from config import Config
import pytest
from app.models import User, Habit, HabitHistory
from datetime import datetime


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4


@pytest.fixture(scope="module")
def test_client():
    app = create_app(TestConfig)
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(username="John", email="john@example.com")
    user2 = User(username="Jane", email="jane@example.com")
    user1.set_password("password")
    user2.set_password("password2")
    db.session.add(user1)
    db.session.add(user2)
    db.session.flush()

    habit1 = Habit(habit="Test Habit 1", user_id=user1.id)
    habit2 = Habit(habit="Test Habit 2", user_id=user2.id)
    db.session.add(habit1)
    db.session.add(habit2)
    db.session.flush()

    habit1_history = HabitHistory(habit_id=habit1.id, timestamp=datetime(2019, 1, 1))
    habit2_history = HabitHistory(habit_id=habit1.id, timestamp=datetime(2019, 1, 2))

    db.session.add(habit1_history)
    db.session.add(habit2_history)
    db.session.flush()

    # Commit the changes for the users

    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


# @pytest.fixture(scope="module")
# def new_user():
#     user = User(username="test_name", email="test_email@example.com")
#     user.set_password("password")
#     return user


# @pytest.fixture(scope="module")
# def new_habit(new_user):
#     """Given the current user, setup a new habbit"""

#     habit = Habit(habit="test_habit", user_id=new_user.id, weekly_goal=3)
#     return habit


# @pytest.fixture(scope="module")
# def new_habit_history(new_habit):
#     """Given a new habit initiate a new log of habit completion"""
#     habit_history = HabitHistory(habit_id=new_habit.id, timestamp=datetime(2019, 1, 1))
#     return habit_history
