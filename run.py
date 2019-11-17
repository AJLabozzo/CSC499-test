from app import create_app, db
from app.models import User, Project, Members, Goals

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Project': Project, 'Goals': Goals, 'Members': Members}

if __name__ == '__main__': 
    app.run()