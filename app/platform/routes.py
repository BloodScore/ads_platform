from app.platform import platform_bp


@platform_bp.route('/', methods=['GET'])
def index():
    return '<h3>Hello from platform_bp<h3>'
