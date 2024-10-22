

from app import db
from models import Marca, Telefono

class MarcaRepositories:
    def get_all(self):
        return Marca.query.all()

    def create(self, nombre):
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        return nueva_marca

    def get_by_id(self, id):
        return Marca.query.get_or_404(id)

    def update(self, marca):
        db.session.commit()

    def get_telefonos_por_marca(self, marca_id):
        marca = self.get_by_id(marca_id)
        return marca.telefonos 