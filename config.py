import os
import psycopg2
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:dontguessmypostgrespassword@34.73.99.129/postgres'
	#disabled tack_modification to not signal the application every time a change is about to be made to the database.
	SQLALCHEMY_TRACK_MODIFICATIONS = False 
	
    # Enable Flask's debugging features. Should be False in production
	DEBUG = True