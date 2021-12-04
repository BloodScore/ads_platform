from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import admin, db, create_app


app = create_app()

from app.auth.models import Role, User
from app.platform.models import Ad, Category


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user in Role.query.filter_by(name='admin').first().users


admin.index_view = AdminModelView
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(Ad, db.session))
admin.add_view(AdminModelView(Category, db.session))


@app.shell_context_processor
def make_shell_context():
    return {
        'Role': Role,
        'User': User,
        'Ad': Ad,
        'Category': Category,
    }
