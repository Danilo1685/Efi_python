from repositories.marca_repositories import MarcaRepositories

class MarcaService:
    def __init__(self, marca_repository: MarcaRepositories):
        self._marca_repository = marca_repository

    def get_all(self):
        return self._marca_repository.get_all()

    def create(self, nombre):
        return self._marca_repository.create(nombre)

    def get_by_id(self, id):
        return self._marca_repository.get_by_id(id)

    def update(self, id, nombre):
        marca = self._marca_repository.get_by_id(id)
        if not marca:
            raise Exception("Marca no encontrada")
        marca.nombre = nombre
        self._marca_repository.update(marca)
        return marca
    
    def get_telefonos_por_marca(self, marca_id):
        return self._marca_repository.get_telefonos_por_marca(marca_id)
