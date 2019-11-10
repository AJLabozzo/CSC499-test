#all page routes for application
from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, ProjectSearchForm, ProjectSubmissionForm, SignupForm, ProfileForm, ProjectForm
from app.models import User, Project, Goals, Members
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
        #need to query for the goals associated with project seperately
        Goalslist = []
        allgoals = Goals.query.filter_by(project_id=data.projectname).all()
        for goal in allgoals:
            Goalslist.append(goal.goal)
        
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

@app.route('/myprojects', methods=['GET', 'POST'])
@login_required
def myprojects():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    projects=[]
    allprojects = Project.query.filter_by(user_id = user.id).all()
    for data in allprojects:
        #need to query for the goals associated with project seperately
        Goalslist = []
        allgoals = Goals.query.filter_by(project_id=data.projectname).all()
        for goal in allgoals:
            Goalslist.append(goal.goal)
        
        if data.progress == False:
            currentstate = "In progress"
        else: 
            currentstate = "Completed"
        
        project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals = Goalslist,status=currentstate,body=data.body)
        projects.append(project)
        
    return render_template('myprojects.html', projects=projects)
    
@app.route('/events')
def events():
	return render_template('events.html')

@app.route('/goal1')
def goals1():
   
    ''' 
    projectID = []
    allprojects = Goals.query.filter_by(goal = 'Zero Hunger').all()
    for project in allprojects:
        projects.append(project)
    
    '''
        
    return render_template('goal1.html')

@app.route('/goal2')
def goals2():
	return render_template('goal2.html')

@app.route('/goal3')
def goals3():
	return render_template('goal3.html')

@app.route('/goal4')
def goals4():
	return render_template('goal4.html')

@app.route('/goal5')
def goals5():
	return render_template('goal5.html')

@app.route('/goal6')
def goals6():
	return render_template('goal6.html')

@app.route('/goal7')
def goals7():
	return render_template('goal7.html')

@app.route('/goal8')
def goals8():
	return render_template('goal8.html')

@app.route('/goal9')
def goals9():
	return render_template('goal9.html')

@app.route('/goal10')
def goals10():
	return render_template('goal10.html')

@app.route('/goal11')
def goals11():
	return render_template('goal11.html')

@app.route('/goal12')
def goals12():
	return render_template('goal12.html')

@app.route('/goal13')
def goals13():
	return render_template('goal13.html')

@app.route('/goal14')
def goals14():
	return render_template('goal14.html')

@app.route('/goal15')
def goals15():
	return render_template('goal15.html')

@app.route('/goal16')
def goals16():
	return render_template('goal16.html')

@app.route('/goal17')
def goals17():
	return render_template('goal17.html')

@app.route('/profile/<username>')
def profile(username):
	user = User.query.filter_by(username=username).first_or_404()
	projects=[]
	allprojects = Project.query.filter_by(user_id = user.id).all()
	for data in allprojects:
        #need to query for the goals associated with project seperately
		Goalslist = []
		allgoals = Goals.query.filter_by(project_id=data.projectname).all()
		for goal in allgoals:
			Goalslist.append(goal.goal)
        
		if data.progress == False:
			currentstate = "In progress"
		else: 
			currentstate = "Completed"
        
		project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals = Goalslist,status=currentstate,body=data.body)
		projects.append(project)
		
	return render_template('myprofile.html', user=user, projects=projects)
	
	
@app.route('/submission_form', methods=['GET', 'POST'])
@login_required
def submission_form():
    form = ProjectSubmissionForm()
    if form.validate_on_submit():
        project = Project(projectname = form.projectname.data, body = form.body.data, user_id = current_user.id, department=form.department.data)
        db.session.add(project) 
        db.session.commit()
        
        goals = request.form.getlist('goals')
        for x in goals:
            goal = Goals(goal=x, project_id=form.projectname.data)
            db.session.add(goal)
            db.session.commit()
        
        projectMembers = request.form.get('members')
        members = projectMembers.split()
        for x in members:
            member = Members(member_id=x, project_id=form.projectname.data)
            db.session.add(member)
            db.session.commit()
        
        return redirect(url_for('projects'))
    return render_template('submission_form.html', form=form)

@app.route('/editProject',methods=['GET','POST'])
@login_required
def editProject():
    form = ProjectForm()
    
    return render_template('editProject.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if request.form.get('fnamebox'):
            current_user.fname = form.fname.data
        if request.form.get('lnamebox'):
            current_user.lname = form.lname.data
        if request.form.get('majorbox'):
            current_user.major = form.major.data
        if request.form.get('minorbox'):
            current_user.minor = form.minor.data
        if request.form.get('aboutbox'):
            current_user.bio = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.major = form.major.data
        current_user.minor = form.minor.data
        form.about.data = current_user.bio
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
