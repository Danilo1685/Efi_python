
from .auth_view import auth_bp
from .marca_view import marca_bp
from .tipo_view import tipo_bp
from .telefono_view import telefono_bp

def register_blueprint(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(tipo_bp)
    app.register_blueprint(telefono_bp)
