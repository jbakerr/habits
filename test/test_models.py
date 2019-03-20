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
    assert habit1.weekly_goal == 1


def test_habit_history(init_database):
    """Given a new habit ensure that logging the habit occured correctly"""
    habit1_history = HabitHistory.query.filter_by(habit_id=1).first()

    assert habit1_history.timestamp == datetime(2019, 1, 1)
    assert habit1_history.__repr__() == "<1 Completed at 2019-01-01 00:00:00>"


def test_complete_habit(init_database):
    """ Given a habit with one completed entry (on 1/1/19) confirm that
    a second entry is recorded on 1/2/19.
    """
    habit1 = Habit.query.filter_by(id=1).first()
    habit1.complete_habit(user_id=1, timestamp=datetime(2019, 1, 2))
    habit1_history = HabitHistory.query.filter_by(habit_id=1).all()
    assert len(habit1_history) == 2


def test_increase_streak(init_database):
    habit1 = Habit.query.filter_by(id=1).first()
    weekly_count = habit1.increase_streak(weekly_count=0)
    assert weekly_count == 1


def test_decrease_streak(init_database):
    habit1 = Habit.query.filter_by(id=1).first()
    weekly_count = habit1.decrease_streak(weekly_count=1)
    assert weekly_count == 0


def test_reset_streak(init_database):
    habit1 = Habit.query.filter_by(id=1).first()
    habit1.reset_current_streak()
    assert habit1.current_streak == 0


def test_reset_longest_streak(init_database):
    habit1 = Habit.query.filter_by(id=1).first()
    habit1.reset_longest_streak()
    assert habit1.longest_streak == 0

