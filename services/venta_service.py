from repositories.venta_repositories import VentaRepositorie, DetalleVentaRepositorie
from app import db

class VentaService:
    def __init__(self):
        self.venta_repo = VentaRepositorie()
        self.detalle_repo = DetalleVentaRepositorie()

    def obtener_ventas(self):
        return self.venta_repo.get_all_ventas() 
    
    def agregar_venta(self, cliente_id, total):
        return self.venta_repo.create_venta(cliente_id, total)

    def agregar_detalle(self, venta_id, telefono_id, cantidad, precio_unitario):
        detalle = self.detalle_repo.create_detalle_venta(venta_id, telefono_id, cantidad, precio_unitario)
        return detalle

    def actualizar_total_venta(self, venta, cantidad, precio_unitario):
        venta.total += int(cantidad) * float(precio_unitario)
        db.session.commit()
