from app import db
from models import Accesorio


class AccesorioRepositories:
    def get_all(self):
        return Accesorio.query.all()

    def create(self, nombre):
        nuevo_accesorio = Accesorio(nombre=nombre)
        db.session.add(nuevo_accesorio)
        db.session.commit()
