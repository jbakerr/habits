from app.models import User, Habit, HabitHistory
from datetime import datetime


#  TODO: Need to leave this in for some reason to load client - look over in future
def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 302


def test_user(init_database):

    user1 = User.query.filter_by(id=1).first()
    user2 = User.query.filter_by(id=2).first()
    assert user1.username == "John"
    assert user1.check_password("password") == True
    assert user1.__repr__() == "<User John>"


def test_new_habit(init_database):
    """ Given the new_user and new_habit ensure that the habit was loaded
    correctly"""

    habit1 = Habit.query.filter_by(id=1).first()
    habit2 = Habit.query.filter_by(id=2).first()

    assert habit1.habit == "Test Habit 1"
    assert habit1.user_id == 1
    assert habit1.__repr__() == "<Habit Test Habit 1>"


def test_habit_history(init_database):
    """Given a new habit ensure that logging the habit occured correctly"""
    habit1_history = HabitHistory.query.filter_by(habit_id=1).first()

    assert habit1_history.timestamp == datetime(2019, 1, 1)
    assert habit1_history.__repr__() == "<1 Completed at 2019-01-01 00:00:00>"
