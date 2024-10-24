
from .auth_view import auth_bp
from .marca_view import marca_bp
from .tipo_view import tipo_bp
from .telefono_view import telefono_bp
from .stock_view import stock_bp
from .accesorio_view import accesorio_bp


from .views_api.accesorios_api import accesorio_app_bp
from .views_api.marca_api import marca_app_bp
from .views_api.tipo_api import tipo_app_bp
from .views_api.stock_api import stock_app_bp
from .views_api.telefono_api import telefono_app_bp
from .views_api.main_api import main_app_bp

def register_blueprint(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(tipo_bp)
    app.register_blueprint(telefono_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(accesorio_bp)

    app.register_blueprint(accesorio_app_bp)
    app.register_blueprint(marca_app_bp)
    app.register_blueprint(tipo_app_bp)
    app.register_blueprint(stock_app_bp)
    app.register_blueprint(telefono_app_bp)
    app.register_blueprint(main_app_bp)
