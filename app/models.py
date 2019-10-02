'''Tables for Database'''

from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	user_role = db.Column(db.Integer,db.ForeignKey('roles.id'))
	admin = db.Column(db.Boolean, unique=False, default=False)
	
	def __repr__(self):
		return '<User {}>'.format(self.username)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(64), index=True, unique=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Project {}>'.format(self.body)

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(64),index=True, unique=True)
    
    def __repr__(self):
        return '<Goals {}>'.format(self.goal)

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64),index=True, unique=True)
    
    def __repr__(self):
        return '<Roles {}>'.format(self.role)