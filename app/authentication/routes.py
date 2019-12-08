#all page routes for application
from flask import flash, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.authentication import bp
from app.authentication.forms import LoginForm, SignupForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from app.authentication.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('authentication.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.landing'))
    return render_template('authentication/login.html', title='Sign In', form=form)

@bp.route('/new_account', methods=['GET', 'POST'])
def new_account():
	if current_user.is_authenticated:
		return redirect(url_for('main.landing'))
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, user_role=form.user_role.data)
		user.set_password(form.password.data)
		if form.user_role.data == 'Admin':
			if form.adminpass.data == 'adminsrock123':
				user.admin = True
			else:
				flash('Incorrect Admin Credentials')
				return redirect(url_for('authentication.new_account'))
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('authentication.login'))
	return render_template('authentication/new_account.html', title='Sign-Up', form=form)

@bp.route('/reset_pass_request', methods=['GET', 'POST'])
def reset_pass_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('authentication.login'))
    return render_template('authentication/reset_pass_request.html',
                           title='Reset Password', form=form)

@bp.route('/reset_pass/<token>', methods=['GET', 'POST'])
def reset_pass(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.landing'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('authentication.login'))
    return render_template('authentication/reset_pass.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.landing'))