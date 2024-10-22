from repositories.tipo_repositories import TipoRepositories

class TipoService:
    def __init__(self, tipo_repository: TipoRepositories):
        self._tipo_repository = tipo_repository

    def get_all(self):
        return self._tipo_repository.get_all()
    
    def create(self, nombre):
        return self._tipo_repository.create(nombre)
    
    def get_by_id(self, id):
        return self._tipo_repository.get_by_id(id)
