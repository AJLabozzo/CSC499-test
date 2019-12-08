import logging
from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
#import flask_whooshalchemy as wa 
 

moment = Moment()
bootstrap = Bootstrap()
db=SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'authentication.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['WHOOSH_BASE'] = 'whoosh'


    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.authentication import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/authentication')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='App Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        
    return app
        
from app import  models