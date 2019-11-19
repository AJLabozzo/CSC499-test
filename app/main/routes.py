#all page routes for application
from flask import flash, render_template, request, redirect, url_for, request, jsonify, current_app, g
from flask_login import current_user, login_required
from app import db
from app.main.forms import ProjectSearchForm, ProjectSubmissionForm, editProfileForm, editProjectForm
from app.main import bp
from app.models import User, Project, Goals, Members
from werkzeug.security import generate_password_hash, check_password_hash
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
		goals = Goals.query.filter_by(project_id=data.projectname).first()
		goalslist=[]
		count = 0
		if goals is not None:
			if goals.g1==True:
				goalslist.append('No Poverty')
		memberslist = []
		allmembers = Members.query.filter_by(project=data.projectname).all()
		for member in allmembers:
			memberslist.append(member.member)   
			
		if data.progress == False:
			currentstate = "In progress"
		else: 
			currentstate = "Completed"
		
		project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals=goalslist, status=currentstate,body=data.body,projectmembers=memberslist)
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
        Goalslist = []
        
            
        memberslist = []
        allmembers = Members.query.filter_by(project=data.projectname).all()
        for member in allmembers:
            memberslist.append(member.member)
        
        if data.progress == False:
            currentstate = "In progress"
        else: 
            currentstate = "Completed"
        
        project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals = Goalslist,status=currentstate,body=data.body,projectmembers=memberslist)
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
	
	memberof = Members.query.filter_by(member=user.username).all()
	if memberof is not None:
		for data in memberof:
			memberproject = Project.query.filter_by(projectname=data.project).all()
			allprojects = allprojects + memberproject
            
	for data in allprojects:
		Goalslist = []
        
		memberslist = []
		allmembers = Members.query.filter_by(project=data.projectname).all()
		for member in allmembers:
			memberslist.append(member.member)
        
		if data.progress == False:
			currentstate = "In progress"
		else: 
			currentstate = "Completed"
        
		project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals = Goalslist,status=currentstate,body=data.body,projectmembers=memberslist)
		projects.append(project)
		
	return render_template('myprofile.html', user=user, projects=projects)
	
	
@bp.route('/submission_form', methods=['GET', 'POST'])
@login_required
def submission_form():
    form = ProjectSubmissionForm()
    if form.validate_on_submit():
        project = Project(projectname = form.projectname.data, body = form.body.data, user_id = current_user.id, department=form.department.data)
        db.session.add(project)
        
        goals = Goals(project_id=form.projectname.data,
                                     g1 = form.g1.data,
                                     g2 = form.g2.data,
                                     g3 = form.g3.data,
                                     g4 = form.g4.data,
                                     g5 = form.g5.data,
                                     g6 = form.g6.data,
                                     g7 = form.g7.data,
                                     g8 = form.g8.data,
                                     g9 = form.g9.data,
                                     g10 = form.g10.data,
                                     g11 = form.g11.data,
                                     g12 = form.g12.data,
                                     g13 = form.g13.data,
                                     g14 = form.g14.data,
                                     g15 = form.g15.data,
                                     g16 = form.g16.data,
                                     g17 = form.g17.data)
        db.session.add(goals)
        
        projectMembers = form.member.data
        member = Members(member=projectMembers, project=form.projectname.data)
        db.session.add(member)
        
        
        db.session.commit()
        return redirect(url_for('main.projects'))
    return render_template('submission_form.html', form=form)

@bp.route('/editProject/<name>',methods=['GET','POST'])
@login_required
def editProject(name):
	form = editProjectForm()
	project = Project.query.filter_by(projectname=name).first()
	member = Members.query.filter_by(project=name).first()
    
	if not current_user.id == project.user_id and current_user.admin==False:
		return redirect(url_for('main.landing'))

	if form.validate_on_submit():
		project = Project(projectname = form.projectname.data, body = form.body.data, user_id = current_user.id, department=form.department.data)
		db.session.add(project)
        
		goalslist = request.form.getlist('goals')
		g = Goals.query.filter_by(project_id=name).first()
		if g == None:
			newGoal = Goals(project_id=form.projectname.data)
			db.session.add(newGoal)
        
		goal = Goals.query.filter_by(project_id=name).first()


		projectMembers = form.member.data
		member = Members(member=projectMembers, project=form.projectname.data)
		db.session.add(member)

		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('main.profile', username=current_user.username))
	elif request.method == 'GET':
		form.projectname.data = project.projectname
		form.body.data = project.body
		form.department.data = project.department
		if member is not None:
			form.member.data = member.member

		goals = Goals.query.filter_by(project_id=name).first()
        
	return render_template('editProject.html', title='Project Edit Form', form=form, project=project, goals=goals)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = editProfileForm()
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