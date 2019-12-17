import os
from dotenv import load_dotenv
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
	#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:dontguessmypostgrespassword@34.73.99.129/postgres'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	#disabled tack_modification to not signal the application every time a change is about to be made to the database.
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
    # Enable Flask's debugging features. Should be False in production
	DEBUG = True
    
	POSTS_PER_PAGE = 20

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['scsu.sustainabilityapp@gmail.com']
