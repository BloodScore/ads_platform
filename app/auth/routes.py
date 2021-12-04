from flask import flash, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_user, logout_user

from werkzeug.urls import url_parse

from app import db
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.auth.models import User
from app.auth.email import send_password_reset_mail, send_account_activation_mail


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('platform.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('auth.login'))
        elif not user.is_active:
            flash(f'Your account is not active! Please check your email for account activation mail. If you don\'t see it send email to {current_app.config["ADMINS"]}')
            return redirect(url_for('auth.login'))
        elif user.is_blocked:
            flash(f'Your account is blocked! For more details send email to {current_app.config["ADMINS"]}')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('platform.index')
            return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('platform.index'))
    else:
        logout_user()
        return redirect(url_for('platform.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('platform.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            password=form.password1.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        flash('Congratulations, you are now a registered user! To activate your account please check your email.')
        send_account_activation_mail(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('platform.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_mail(user)
        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('platform.index'))
    user = User.verify_jwt_token(token)
    if not user:
        return redirect(url_for('platform.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password1.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/activate_account/<token>', methods=['GET', 'POST'])
def activate_account(token):
    if current_user.is_authenticated:
        return redirect(url_for('platform.index'))
    user = User.verify_jwt_token(token)
    if not user:
        return redirect(url_for('platform.index'))
    user.update(is_active=True)
    flash('Your account has been activated.')
    return redirect(url_for('auth.login'))
