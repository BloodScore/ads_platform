from flask import Blueprint


platform_bp = Blueprint('platform', __name__)

from app.platform import routes
