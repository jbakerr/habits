from app import create_app
from config import Config
import pytest


# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))


@pytest.fixture()
def app():
    app = create_app(Config)
    return app
