from flask import url_for
from app.models import User
import pytest


@pytest.fixture(scope = 'module')
def new_user():
    user = User(username='test_name', email='test_email@example.com')
    user.set_password('password')
    return user


# Ensure index page redicts for a user not logged in
def test_load(client):
    assert client.get(url_for('main.index')).status_code == 302



def test_new_user(new_user):
    """Given a new user ensure that user is created correctly,
    password is hashed, and user can be authenicated
    """

    assert new_user.username == 'test_name'
    assert new_user.password_hash != "password"
    assert new_user.email == 'test_email@example.com'
    assert new_user.check_password(password ='password') == True



