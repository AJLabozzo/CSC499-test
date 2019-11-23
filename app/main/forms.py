from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, RadioField
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
    g1 = BooleanField('')
    g2 = BooleanField('')
    g3 = BooleanField('')
    g4 = BooleanField('')
    g5 = BooleanField('')
    g6 = BooleanField('')
    g7 = BooleanField('')
    g8 = BooleanField('')
    g9 = BooleanField('')
    g10 = BooleanField('')
    g11 = BooleanField('')
    g12 = BooleanField('')
    g13 = BooleanField('')
    g14 = BooleanField('')
    g15 = BooleanField('')
    g16 = BooleanField('')
    g17 = BooleanField('')
    member = StringField('',validators=[Length(max=64)])
    submit = SubmitField('Submit')
    
    def validate_projectname(self, projectname):
        name = Project.query.filter_by(projectname=projectname.data).first()
        if name is not None:
            raise ValidationError('Please use a different title.')
    
    def validate_member(self, member):
        user = User.query.filter_by(username=member.data).first()
        if user is None:
            raise ValidationError('User does not exist.')

class editProjectForm(FlaskForm):
    projectname = StringField('',validators=[Length(max=64)])
    body = TextAreaField('',validators=[Length(max=500)])
    department = StringField('',validators=[Length(max=64)])
    g1 = BooleanField('')
    g2 = BooleanField('')
    g3 = BooleanField('')
    g4 = BooleanField('')
    g5 = BooleanField('')
    g6 = BooleanField('')
    g7 = BooleanField('')
    g8 = BooleanField('')
    g9 = BooleanField('')
    g10 = BooleanField('')
    g11 = BooleanField('')
    g12 = BooleanField('')
    g13 = BooleanField('')
    g14 = BooleanField('')
    g15 = BooleanField('')
    g16 = BooleanField('')
    g17 = BooleanField('')
    member = StringField('',validators=[Length(max=64)])
    status = BooleanField('')
    submit = SubmitField('Submit')
    
    
    def validate_member(self, member):
        user = User.query.filter_by(username=member.data).first()
        if user is None:
            raise ValidationError('User does not exist.')
    
class editProfileForm(FlaskForm):
	fname = StringField('first name', validators=[Length(max=64)])
	lname = StringField('last name', validators=[Length(max=64)])
	major = StringField('your major', validators=[Length(max=64)])
	minor = StringField('minor - if any', validators=[Length(max=64)])
	about = TextAreaField('About me', validators=[Length(min=0, max=500)])
	submit	= SubmitField('Submit')


class UserSearchForm(FlaskForm):
    choices = [('Student', 'Student'),
               ('Faculty', 'Faculty'),
               ('Staff', 'Staff'),
               ('Department', 'Department')]
        
    select = SelectField('', choices=choices)
    search = StringField('')

class editUserAdminViewForm(FlaskForm):
    fname = StringField('first name', validators=[Length(max=64)])
    lname = StringField('last name', validators=[Length(max=64)])
    admin = BooleanField('')
    submit	= SubmitField('Submit')
