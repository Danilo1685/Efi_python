from app import db
from models import Tipo


class TipoRepositories:
    def get_all(self):
        return Tipo.query.all()
    
    def create(self, nombre):
        nuevo_tipo = Tipo(nombre=nombre)
        db.session.add(nuevo_tipo)
        db.session.commit()
        return nuevo_tipo
    
    def get_by_id(self, id):
        return Tipo.query.filter_by(id=id).first()
