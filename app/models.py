from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
import jwt

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	user_role = db.Column(db.String(64))
	admin = db.Column(db.Boolean, unique=False, default=False)
	fname = db.Column(db.String(64))
	lname = db.Column(db.String(64))
	major = db.Column(db.String(64))
	minor = db.Column(db.String(64))
	bio =  db.Column(db.String(500))
	department = db.Column(db.String(64))
    
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
    
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)
    
	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
							app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(64), index=True, unique=True)
    body = db.Column(db.String(500),unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    department = db.Column(db.String(64))
    progress = db.Column(db.Boolean, unique=False, default=False)
    
    def __repr__(self):
        return '<Project {}>'.format(self.projectname)

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(64))
    project_id = db.Column(db.String(64))
    
    def __repr__(self):
        return '<Members {}>'.format(self.member_id)

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(64))
    project_id = db.Column(db.String(64))
    
    def __repr__(self):
        return '<Goals {}>'.format(self.goal)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))