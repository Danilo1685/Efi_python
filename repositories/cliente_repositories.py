from app import db
from models import Cliente

class ClienteRepositorie:
    def get_all(self):
        return Cliente.query.all()

    def get_by_id(self, cliente_id):
        return Cliente.query.get_or_404(cliente_id)

    def add(self, cliente):
        db.session.add(cliente)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, cliente):
        db.session.delete(cliente)
        db.session.commit()
