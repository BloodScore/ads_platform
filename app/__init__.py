from flask import Flask

from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config


admin = Admin(template_mode='bootstrap3')
bootstrap = Bootstrap()
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()
migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__,
                static_folder='static')
    app.config.from_object(config_class)

    admin.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from app.platform import platform_bp
    app.register_blueprint(platform_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
