from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models import User, Project



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
