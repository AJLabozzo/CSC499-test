from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(),Length(max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username does not exist.')
    
    
class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),Length(max=64)])
	email = StringField('Email', validators=[DataRequired(), Email(),Length(max=120)])
	user_role = SelectField('User Role',choices=[('Sudent', 'Sudent'), 
												 ('Faculty', 'Faculty'), 
												 ('Staff', 'Staff'), 
												 ('Admin','Admin')])
	password = PasswordField('Password', validators=[DataRequired(),Length(max=128)])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	adminpass = PasswordField('Admin Credentials',validators=[Length(max=64)])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')
    
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email does not belong to any accounts.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Submit')
