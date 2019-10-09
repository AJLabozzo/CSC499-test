#all page routes for application
from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm, ProjectSearchForm
from app.models import User
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
    if request.method == 'Post':
        return search_results(search)
    return render_template('projects.html', form=search)

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

@app.route('/myprofile')
def myprofile():
	return render_template('myprofile.html')

@app.route('/submission_form')
def submission_form():
	return render_template('submission_form.html')

@app.route('/login', methods=['Get','Post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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