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
		if goals is not None:
			if goals.g1==True:
				goalslist.append('No Poverty')
			if goals.g2==True:
				goalslist.append('Zero Hunger')
			if goals.g3==True:
				goalslist.append('Good Health & Well-Being')
			if goals.g4==True:
				goalslist.append('Quality Education')
			if goals.g5==True:
				goalslist.append('Gender Equality')
			if goals.g6==True:
				goalslist.append('Clean Water & Sanitation')
			if goals.g7==True:
				goalslist.append('Affordable & Clean Energy')
			if goals.g8==True:
				goalslist.append('Decent Work & Economic Growth')
			if goals.g9==True:
				goalslist.append('Industry, Innovation, and Infrastructure')
			if goals.g10==True:
				goalslist.append('Reduced Inequalities')
			if goals.g11==True:
				goalslist.append('Sustainable Cities and Communities')
			if goals.g12==True:
				goalslist.append('Responsible Consumption and Production')
			if goals.g13==True:
				goalslist.append('Climate Action')
			if goals.g14==True:
				goalslist.append('Life Below Water')
			if goals.g15==True:
				goalslist.append('Life on Land')
			if goals.g16==True:
				goalslist.append('Peace & Justice Strong Institutions')
			if goals.g17==True:
				goalslist.append('Partnerships for the Goals')
                
        
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
        project = dict(projectname=data.projectname)
        projects.append(project)
        
    return render_template('myprojects.html', projects=projects)
    
@bp.route('/events')
def events():
	return render_template('events.html')

@bp.route('/goal/<goal>')
def goal(goal):
	projectsbygoal = []
	if goal == 'No Poverty':
		getprojects = Goals.query.filter_by(g1=True).all()
	elif goal == 'Zero Hunger':
		getprojects = Goals.query.filter_by(g2=True).all()
	elif goal == 'Good Health & Well-Being':
		getprojects = Goals.query.filter_by(g3=True).all()
	elif goal == 'Quality Education':
		getprojects = Goals.query.filter_by(g4=True).all()
	elif goal == 'Gender Equality':
		getprojects = Goals.query.filter_by(g5=True).all()
	elif goal == 'Clean Water & Sanitation':
		getprojects = Goals.query.filter_by(g6=True).all()
	elif goal == 'Affordable & Clean Energy ':
		getprojects = Goals.query.filter_by(g7=True).all()
	elif goal == 'Decent Work & Economic Growth':
		getprojects = Goals.query.filter_by(g8=True).all()
	elif goal == 'Industry, Innovation, and Infrastructure':
		getprojects = Goals.query.filter_by(g9=True).all()
	elif goal == 'Reduced Inequalities':
		getprojects = Goals.query.filter_by(g10=True).all()
	elif goal == 'Sustainable Cities and Communities':
		getprojects = Goals.query.filter_by(g11=True).all()
	elif goal == 'Responsible Consumption and Production':
		getprojects = Goals.query.filter_by(g12=True).all()
	elif goal == 'Climate Action ':
		getprojects = Goals.query.filter_by(g13=True).all()
	elif goal == 'Life Below Water':
		getprojects = Goals.query.filter_by(g14=True).all()
	elif goal == 'Life on Land':
		getprojects = Goals.query.filter_by(g15=True).all()
	elif goal == 'Peace & Justice Strong Institutions':
		getprojects = Goals.query.filter_by(g16=True).all()
	else:
		getprojects = Goals.query.filter_by(g17=True).all()

	for item in getprojects:
		projectsbygoal.append(item)
    
	allprojects = []
	for data in projectsbygoal:
		
		currentproject = Project.query.filter_by(projectname = data.project_id).first()
		goals = Goals.query.filter_by(project_id=currentproject.projectname).first()

		goalslist=[]
		if goals is not None:
			if goals.g1==True:
				goalslist.append('No Poverty')
			if goals.g2==True:
				goalslist.append('Zero Hunger')
			if goals.g3==True:
				goalslist.append('Good Health & Well-Being')
			if goals.g4==True:
				goalslist.append('Quality Education')
			if goals.g5==True:
				goalslist.append('Gender Equality')
			if goals.g6==True:
				goalslist.append('Clean Water & Sanitation')
			if goals.g7==True:
				goalslist.append('Affordable & Clean Energy')
			if goals.g8==True:
				goalslist.append('Decent Work & Economic Growth')
			if goals.g9==True:
				goalslist.append('Industry, Innovation, and Infrastructure')
			if goals.g10==True:
				goalslist.append('Reduced Inequalities')
			if goals.g11==True:
				goalslist.append('Sustainable Cities and Communities')
			if goals.g12==True:
				goalslist.append('Responsible Consumption and Production')
			if goals.g13==True:
				goalslist.append('Climate Action')
			if goals.g14==True:
				goalslist.append('Life Below Water')
			if goals.g15==True:
				goalslist.append('Life on Land')
			if goals.g16==True:
				goalslist.append('Peace & Justice Strong Institutions')
			if goals.g17==True:
				goalslist.append('Partnerships for the Goals')

		memberslist = []
		allmembers = Members.query.filter_by(project=currentproject.projectname).all()
		for member in allmembers:
			memberslist.append(member.member)

		if currentproject.progress == False:
			currentstate = "In progress"
		else: 
			currentstate = "Completed"
			
		projectdict = dict(projectname=currentproject.projectname,department=currentproject.department,username=User.query.get(currentproject.user_id).username,status=currentstate,goals=goalslist,body=currentproject.body,projectmembers=memberslist)
		allprojects.append(projectdict)
		
	return render_template('goalbase.html', goal=goal, projects = allprojects)
    
@bp.route('/profile/<username>')
def profile(username):
	user = User.query.filter_by(username=username).first_or_404()
	
	badges=[]
	projects=[]
	allprojects = Project.query.filter_by(user_id = user.id).all()
	
	memberof = Members.query.filter_by(member=user.username).all()
	if memberof is not None:
		for data in memberof:
			memberproject = Project.query.filter_by(projectname=data.project).all()
			allprojects = allprojects + memberproject
    
	for data in allprojects:
		goalslist=[]
		goals = Goals.query.filter_by(project_id=data.projectname).first()
		if goals is not None:
			if goals.g1==True:
				goalslist.append('No Poverty')
			if goals.g2==True:
				goalslist.append('Zero Hunger')
			if goals.g3==True:
				goalslist.append('Good Health and Well-Being')
			if goals.g4==True:
				goalslist.append('Quality Education')
			if goals.g5==True:
				goalslist.append('Gender Equality')
			if goals.g6==True:
				goalslist.append('Clean Water & Sanitation')
			if goals.g7==True:
				goalslist.append('Affordable & Clean Energy')
			if goals.g8==True:
				goalslist.append('Decent Work & Economic Growth')
			if goals.g9==True:
				goalslist.append('Industry, Innovation, and Infrastructure')
			if goals.g10==True:
				goalslist.append('Reduced Inequalities')
			if goals.g11==True:
				goalslist.append('Sustainable Cities and Communities')
			if goals.g12==True:
				goalslist.append('Responsible Consumption and Production')
			if goals.g13==True:
				goalslist.append('Climate Action')
			if goals.g14==True:
				goalslist.append('Life Below Water')
			if goals.g15==True:
				goalslist.append('Life on Land')
			if goals.g16==True:
				goalslist.append('Peace & Justice Strong Institutions')
			if goals.g17==True:
				goalslist.append('Partnerships for the Goals')
        
		memberslist = []
		allmembers = Members.query.filter_by(project=data.projectname).all()
		for member in allmembers:
			memberslist.append(member.member)
        
		if data.progress == False:
			currentstate = "In progress"
		else: 
			currentstate = "Completed"
			if goals.g1==True:
				badges.append('1')
			if goals.g2==True:
				badges.append('2')
			if goals.g3==True:
				badges.append('3')
			if goals.g4==True:
				badges.append('4')
			if goals.g5==True:
				badges.append('5')
			if goals.g6==True:
				badges.append('6')
			if goals.g7==True:
				badges.append('7')
			if goals.g8==True:
				badges.append('8')
			if goals.g9==True:
				badges.append('9')
			if goals.g10==True:
				badges.append('10')
			if goals.g11==True:
				badges.append('11')
			if goals.g12==True:
				badges.append('12')
			if goals.g13==True:
				badges.append('13')
			if goals.g14==True:
				badges.append('14')
			if goals.g15==True:
				badges.append('15')
			if goals.g16==True:
				badges.append('16')
			if goals.g17==True:
				badges.append('17')
            
        
		project = dict(projectname=data.projectname,department=data.department,username=User.query.get(data.user_id).username,goals = goalslist,status=currentstate,body=data.body,projectmembers=memberslist)
		projects.append(project)
        
	noDuplicates=[]
	for x in badges:
		if x not in noDuplicates:
			noDuplicates.append(x)
	badges = noDuplicates
        
        
	return render_template('myprofile.html', user=user, projects=projects, badges=badges)
	
	
@bp.route('/submission_form', methods=['GET', 'POST'])
@login_required
def submission_form():
	form = ProjectSubmissionForm()
	if form.validate_on_submit():
		project = Project(projectname = form.projectname.data, body = form.body.data, user_id = current_user.id, department=form.department.data)
		db.session.add(project)
		
		if form.g1.data:
			g1 = True
		else:
			g1 = False
		if form.g2.data:
			g2 = True
		else:
			g2 = False
		if form.g3.data:
			g3 = True
		else:
			g3 = False
		if form.g4.data:
			g4 = True
		else:
			g4 = False
		if form.g5.data:
			g5 = True
		else:
			g5 = False
		if form.g6.data:
			g6 = True
		else:
			g6 = False
		if form.g7.data:
			g7 = True
		else:
			g7 = False
		if form.g8.data:
			g8 = True
		else:
			g8 = False
		if form.g9.data:
			g9 = True
		else:
			g9 = False
		if form.g10.data:
			g10 = True
		else:
			g10 = False
		if form.g11.data:
			g11 = True
		else:
			g11 = False
		if form.g12.data:
			g12 = True
		else:
			g12 = False
		if form.g13.data:
			g13 = True
		else:
			g13 = False
		if form.g14.data:
			g14 = True
		else:
			g14 = False
		if form.g15.data:
			g15 = True
		else:
			g15 = False
		if form.g16.data:
			g16 = True
		else:
			g16 = False
		if form.g17.data:
			g17 = True
		else:
			g17 = False
		goals = Goals(project_id=form.projectname.data,g1=g1,g2=g2,g3=g3,g4=g4,g5=g5,g6=g6,g7=g7,g8=g8,g9=g9,g10=g10,g11=g11,g12=g12,g13=g13,g14=g14,g15=g15,g16=g16,g17=g17)
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
	goals = Goals.query.filter_by(project_id=name).first()
    
	if not current_user.id == project.user_id and current_user.admin==False:
		return redirect(url_for('main.landing'))

	if form.validate_on_submit():
        
		if not project.projectname == form.projectname.data:
			namecheck = Project.query.filter_by(projectname=form.projectname.data).first()
			if namecheck is None:
				project.projectname = form.projectname.data
		project.body = form.body.data
		project.department = form.body.data
        
		if form.g1.data:
			goals.g1 = form.g1.data
		else:
			goals.g1 = False
		if form.g2.data:
			goals.g2 = form.g2.data
		else:
			goals.g2 = False
		if form.g3.data:
			goals.g3 = form.g3.data
		else:
			goals.g3 = False
		if form.g4.data:
			goals.g4 = form.g4.data
		else:
			goals.g4 = False
		if form.g5.data:
			goals.g5 = form.g5.data
		else:
			goals.g5 = False
		if form.g6.data:
			goals.g6 = form.g6.data
		if form.g7.data:
			goals.g7 = form.g7.data
		else:
			goals.g7 = False
		if form.g8.data:
			goals.g8 = form.g8.data
		else:
			goals.g8 = False
		if form.g9.data:
			goals.g9 = form.g9.data
		else:
			goals.g9 = False
		if form.g10.data:
			goals.g10 = form.g10.data
		else:
			goals.g10 = False
		if form.g11.data:
			goals.g11 = form.g11.data
		else:
			goals.g11 = False
		if form.g12.data:
			goals.g12 = form.g12.data
		else:
			goals.g12 = False
		if form.g13.data:
			goals.g13 = form.g13.data
		else:
			goals.g13 = False
		if form.g14.data:
			goals.g14 = form.g14.data
		else:
			goals.g15 = False
		if form.g15.data:
			goals.g15 = form.g15.data
		else:
			goals.g15 = False
		if form.g16.data:
			goals.g16 = form.g16.data
		else:
			goals.g16 = False
		if form.g17.data:
			goals.g17 = form.g17.data
		else:
			goals.g17 = False
		member.member = form.member.data
        
		if form.status.data:
			project.progress = True
		else:
			project.progress = False

		db.session.commit()
        
		flash('Your changes have been saved.')
		return redirect(url_for('main.profile', username=current_user.username))
	elif request.method == 'GET':
		form.projectname.data = project.projectname
		form.body.data = project.body
		form.department.data = project.department
		if member is not None:
			form.member.data = member.member
        
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