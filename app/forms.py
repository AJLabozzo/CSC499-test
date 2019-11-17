from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models import User, Project

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(),Length(max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(),Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(),Length(max=128)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
class ProjectSearchForm(FlaskForm):
    choices = [('Goal', 'Goal'),
               ('Faculty', 'Faculty'),
               ('Department', 'Department')]
        
    select = SelectField('', choices=choices)
    search = StringField('')
    
class ProjectSubmissionForm(FlaskForm):
    projectname = StringField('',validators=[DataRequired(),Length(max=64)])
    body = TextAreaField('',validators=[DataRequired(),Length(max=500)])
    department = StringField('',validators=[DataRequired(),Length(max=64)])
    members = StringField('',validators=[Length(max=64)])
    submit = SubmitField('Submit')
    
    def validate_projectname(self, projectname):
        name = Project.query.filter_by(projectname=projectname.data).first()
        if name is not None:
            raise ValidationError('Please use a different title.')

class ProjectForm(FlaskForm):
    projectname = StringField('',validators=[Length(max=64)])
    body = TextAreaField('',validators=[Length(max=500)])
    department = StringField('',validators=[Length(max=64)])
    members = StringField('',validators=[Length(max=64)])
    submit = SubmitField('Submit')
    
    def validate_projectname(self, projectname):
        name = Project.query.filter_by(projectname=projectname.data).first()
        if name is not None:
            raise ValidationError('Please use a different title.')
    
class ProfileForm(FlaskForm):
	fname = StringField('first name', validators=[Length(max=64)])
	lname = StringField('last name', validators=[Length(max=64)])
	major = StringField('your major', validators=[Length(max=64)])
	minor = StringField('minor - if any', validators=[Length(max=64)])
	about = TextAreaField('About me', validators=[Length(min=0, max=500)])
	submit	= SubmitField('Submit')