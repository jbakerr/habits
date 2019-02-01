from flask import url_for
from app.models import User


# Ensure index page loads correctly
def test_landing(client):
    assert client.get(url_for('main.index')).status_code == 200


def test_new_user():
    """Given a new user ensure that user is updated in db,
    password is hashed, and user can be authenicated
    """

    user = User(username='test_name', email='test_email@example.com')
    user.set_password('password')
    assert user.username == 'test_name'
    assert user.password_hash != "password"
    assert user.email == 'test_email@example.com'


