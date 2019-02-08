from app import create_app, db
from app.models import User, Habbit, HabbitHistory

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Habbit': Habbit, 'HabbitHistory': HabbitHistory}
