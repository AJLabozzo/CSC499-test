import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
	#disabled tack_modification to not signal the application every time a change is about to be made to the database.
	SQLALCHEMY_TRACK_MODIFICATIONS = False 
	
    # Enable Flask's debugging features. Should be False in production
	DEBUG = True