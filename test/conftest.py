from app import create_app
from config import Config
import pytest

@pytest.fixture
def app():
    app = create_app(Config)
    return app

