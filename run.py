from app import app, db
from app.models import User, Project, Goals, Roles

'''
following function adds the database instance and models to python shell sessions
for testing purposes. This way we can work with the database entities  without having
to import them. command: flask shell (while venv active)
'''
@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Project': Project, 'Goals': Goals, 'Roles': Roles}

if __name__ == '__main__':
    app.run()