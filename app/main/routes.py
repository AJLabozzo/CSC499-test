#all page routes for application
from flask import flash, render_template, request, redirect, url_for, request, jsonify, current_app, g
from flask_login import current_user, login_required
from app import db
from app.main.forms import ProjectSearchForm, ProjectSubmissionForm, ProfileForm, ProjectForm
from app.main import bp
from app.models import User, Project, Goals, Members
from werkzeug.security import generate_password_hash, check_password_hash
from app.email import send_password_reset_email
from datetime import datetime


@bp.route('/')
@bp.route('/index')
def landing():
	return render_template('landing.html')

@bp.route('/base')
@login_required
def base():
	return render_template('main.base.html')
	
@bp.route('/goals')
def goals():
	return render_template('goals.html')

@bp.route('/projects', methods=['GET','POST'])
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

@bp.route('/myprojects', methods=['GET', 'POST'])
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
    
@bp.route('/events')
def events():
	return render_template('events.html')

@bp.route('/goal/<goal>')
def goal(goal):
    projectsbygoal = []
    getprojects = Goals.query.filter_by(goal=goal).all()
    for item in getprojects:
        projectsbygoal.append(item)
    
    allprojects = []
    for data in projectsbygoal:
        
        currentproject = Project.query.filter_by(projectname = data.project_id).first()
        
        if currentproject.progress == False:
            currentstate = "In progress"
        else: 
            currentstate = "Completed"
            
        projectdict = dict(projectname=currentproject.projectname,department=currentproject.department,username=User.query.get(currentproject.user_id).username,status=currentstate,body=currentproject.body)
        allprojects.append(projectdict)
        
    return render_template('goalbase.html', goal=goal, projects = allprojects)
    
@bp.route('/profile/<username>')
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
	
	
@bp.route('/submission_form', methods=['GET', 'POST'])
@login_required
def submission_form():
    form = ProjectSubmissionForm()
    if form.validate_on_submit():
        project = Project(projectname = form.projectname.data, body = form.body.data, user_id = current_user.id, department=form.department.data)
        db.session.add(project) 
        db.session.commit()
        
        goals = request.form.getlist('main.goals')
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
        
        return redirect(url_for('main.projects'))
    return render_template('submission_form.html', form=form)

@bp.route('/editProject/<name>',methods=['GET','POST'])
@login_required
def editProject(name):
    form = ProjectForm()
    project = Project.query.filter_by(projectname=name).first()
    if form.validate_on_submit():
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.profile', username=current_user.username))
    elif request.method == 'GET':
        form.projectname.data = project.projectname
        form.body.data = project.body
        form.department.data = project.department
    return render_template('editProject.html', form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.major = form.major.data
        current_user.minor = form.minor.data
        current_user.bio = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.major.data = current_user.major
        form.minor.data = current_user.minor
        form.about.data = current_user.bio
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)