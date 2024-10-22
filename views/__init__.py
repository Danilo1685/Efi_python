
from .auth_view import auth_bp
from .marca_view import marca_bp
from .tipo_view import tipo_bp
from .telefono_view import telefono_bp
from .venta_view import ventas_bp
from .cliente_view import cliente_bp
from .stock_view import stock_bp
from .accesorio_view import accesorio_bp


from .views_api.accesorios_api import accesorio_app_bp
def register_blueprint(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(tipo_bp)
    app.register_blueprint(telefono_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(accesorio_bp)

    app.register_blueprint(accesorio_app_bp)