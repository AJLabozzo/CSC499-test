#all page routes for application
from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, ProjectSearchForm, ProjectSubmissionForm, SignupForm
from app.models import User, Project, Goals
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/index')
def landing():
	return render_template('landing.html')

@app.route('/base')
def base():
	return render_template('base.html')
	
@app.route('/goals')
def goals():
	return render_template('goals.html')

@app.route('/projects', methods=['GET','POST'])
def projects():
    
    search = ProjectSearchForm(request.form)
    projects=[]
    
    if request.method == 'Post':
        return render_template('projects.html')
    
    allprojects = Project.query.all()
    for data in allprojects:
        #need to query for the goals associated with project sperately
        Goalslist = []
        allgoals = Goals.query.filter_by(project_id=data.projectname).all()
        for goal in allgoals:
            Goalslist.append(goal)
        
        if data.progress == False:
            currentstate = "In progress"
        else: 
            currentstate = "Completed"
        
        project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals = Goalslist,status=currentstate,body=data.body)
        projects.append(project)
    
    return render_template('projects.html', form=search, projects=projects)

def search_results(search):
    results = []
    search_string = search.data['search']
 
    if search.data['search'] == '':
        qry = Project.query.all()
        results = qry
 
    if not results:
        flash('No results found!')
        return redirect('/projects')
    else:
        table = Results(results)
        return render_template('projects.html', form=search, table=table)

@app.route('/events')
def events():
	return render_template('events.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/goal1')
def goals1():
	return render_template('goal1.html')

@app.route('/profile/<username>')
def profile(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('myprofile.html', user=user)
	
	
@app.route('/submission_form', methods=['GET', 'POST'])
@login_required
def submission_form():
    form = ProjectSubmissionForm()
    if form.validate_on_submit():
        project = Project(projectname = form.projectname.data, body = form.body.data, user_id = current_user.id, department=request.form.get('department'))
        db.session.add(project) 
        db.session.commit()
        
        goals = request.form.getlist('goals')
        for x in goals:
            goal = Goals(goal=x, project_id=form.projectname.data)
            db.session.add(goal)
            db.session.commit()
        return redirect(url_for('projects'))
    return render_template('submission_form.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
    
@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_role=request.form.get('user_role'))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('landing'))
    return render_template('new_account.html', title='Sign-Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('landing'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing'))

'''
@app.route('/myProfile/<username>')
@login_required
def profile(username):
	return render_template('profile.html')
	'''
