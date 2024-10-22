from models import Accesorio
from app import db

class AccesorioRepositorie:
    def get_all(self):
        return Accesorio.query.all()

    def get_by_id(self, id):
        return Accesorio.query.get_or_404(id)

    def create(self, nombre):
        accesorio = Accesorio(nombre=nombre)
        db.session.add(accesorio)
        db.session.commit()

    def update(self, id, nombre):
        accesorio = self.get_by_id(id)
        accesorio.nombre = nombre
        db.session.commit()

    def delete(self, id):
        accesorio = self.get_by_id(id)
        db.session.delete(accesorio)
        db.session.commit()
