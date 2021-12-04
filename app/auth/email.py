from flask import current_app, render_template
from utils.mail import send_mail


def send_password_reset_mail(user):
    token = user.get_jwt_token()
    send_mail(
        '[ADS Platform] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password_mail.txt', user=user, token=token),
        html_body=render_template('email/reset_password_mail.html', user=user, token=token)
    )


def send_account_activation_mail(user):
    token = user.get_jwt_token()
    send_mail(
        '[ADS Platform] Activate Your Account',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/activate_account_mail.txt', user=user, token=token),
        html_body=render_template('email/activate_account_mail.html', user=user, token=token)
    )
