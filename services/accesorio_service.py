from repositories.accesorio_repositories import AccesorioRepositories

class AccesorioService:
    def __init__(self, accesorio_repository):
        self.accesorio_repository = accesorio_repository

    def get_all(self):
        return self.accesorio_repository.get_all()

    def create(self, nombre):
        self.accesorio_repository.create(nombre)
