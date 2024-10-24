from app import db
from models import Telefono, Telefono_Accesorio

class TelefonoRepositories:
    def get_all(self):
        return Telefono.query.all()

    def create(self, modelo, anio_fabricacion, precio, marca, tipo):
        nuevo_telefono = Telefono(modelo=modelo, anio_fabricacion=anio_fabricacion, precio=precio, marca_id=marca, tipo_id=tipo)
        db.session.add(nuevo_telefono)
        db.session.commit()
        return nuevo_telefono

    def get_by_id(self, id):
        return Telefono.query.get_or_404(id)

    def get_accesorios_by_telefono(self, telefono_id):
        return [ta.accesorio for ta in Telefono_Accesorio.query.filter_by(telefono_id=telefono_id).all()]

