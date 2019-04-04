def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_login(test_client, init_database):

    response = test_client.post(
        "/login",
        form=dict(username="John@gmail.com", password="password"),
        follow_redirects=True,
    )
    assert response.status_code == 200
