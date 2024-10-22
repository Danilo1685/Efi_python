# services/cliente_service.py

from repositories.cliente_repositories import ClienteRepositorie
from models import Cliente

class ClienteService:
    def __init__(self):
        self.repositorio = ClienteRepositorie()  

    def obtener_todos_los_clientes(self):
        return self.repositorio.get_all()  

    def obtener_cliente_por_id(self, cliente_id):
        return self.repositorio.get_by_id(cliente_id)  

    def crear_cliente(self, datos):
        nuevo_cliente = Cliente(**datos)
        self.repositorio.add(nuevo_cliente)  
        return nuevo_cliente

    def actualizar_cliente(self, cliente_id, datos):
        cliente = self.repositorio.get_by_id(cliente_id)  
        cliente.nombre = datos.get('nombre')
        cliente.correo = datos.get('correo')
        cliente.telefono = datos.get('telefono')
        cliente.direccion = datos.get('direccion')
        self.repositorio.update(cliente)  
        return cliente

    def eliminar_cliente(self, cliente_id):
        cliente = self.repositorio.get_by_id(cliente_id) 
        self.repositorio.delete(cliente)  
