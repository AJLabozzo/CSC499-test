from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EMail, Equalto, ValidationError
from app.models import User, Project

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(),Length(max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
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
    submit = SubmitField('Submit')
    
    def validate_projectname(self, projectname):
        name = Project.query.filter_by(projectname=projectname.data).first()
        if name is not None:
            raise ValidationError('Please use a different title.')