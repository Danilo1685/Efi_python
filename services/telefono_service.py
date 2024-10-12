from app import db
from repositories.telefono_repositories import TelefonoRepositories
from models import Telefono, DetalleVenta ,Stock

class TelefonoService:
    def __init__(self, telefono_repository: TelefonoRepositories):
        self._telefono_repository = telefono_repository

    def get_all(self):
        return self._telefono_repository.get_all()

    def create(self, modelo, anio_fabricacion, precio, marca, tipo):
        return self._telefono_repository.create(modelo, anio_fabricacion, precio, marca, tipo)

    def get_by_id(self, id):
        return self._telefono_repository.get_by_id(id)

    def delete_with_accesorios(self, id):
        telefono = self._telefono_repository.get_by_id(id)
        
        for stock in telefono.stocks:
            stock.cantidad -= 1
            if stock.cantidad <= 0:
                db.session.delete(stock)
        
        for accesorio in telefono.accesorios:
            db.session.delete(accesorio)
        
        db.session.delete(telefono)
        db.session.commit()

    def get_accesorios_by_telefono(self, telefono_id):
        return self._telefono_repository.get_accesorios_by_telefono(telefono_id)

def delete_with_accesorios(telefono_id):
    # Asegúrate de eliminar las asociaciones o actualizarlas
    detalle_ventas = DetalleVenta.query.filter_by(telefono_id=telefono_id).all()
    if detalle_ventas:
        for detalle in detalle_ventas:
            # Decide qué hacer: eliminar detalle o asignar nuevo telefono_id
            db.session.delete(detalle)  # Elimina el detalle de la venta

    # Actualiza el telefono_id en stock a None o a un valor por defecto
    # Supongo que tienes una tabla `stock` y `telefono_id` es una clave foránea.
    stock_items = Stock.query.filter_by(telefono_id=telefono_id).all()
    for item in stock_items:
        item.telefono_id = None  # o asigna un nuevo telefono_id válido
        db.session.add(item)

    # Luego, elimina el teléfono
    telefono = Telefono.query.get(telefono_id)
    db.session.delete(telefono)

    # Realiza el commit
    db.session.commit()



