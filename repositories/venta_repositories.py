from models import db, Venta, DetalleVenta

class VentaRepositorie:
    def __init__(self):
        pass

    def get_all_ventas(self):
        return Venta.query.all()

    def get_venta_by_id(self, venta_id):
        return Venta.query.get_or_404(venta_id)

    def create_venta(self, cliente_id, total):
        nueva_venta = Venta(cliente_id=cliente_id, total=total)
        db.session.add(nueva_venta)
        db.session.commit()
        return nueva_venta


class DetalleVentaRepositorie:
    def __init__(self):
        pass

    def create_detalle_venta(self, venta_id, telefono_id, cantidad, precio_unitario):
        detalle = DetalleVenta(
            venta_id=venta_id,
            telefono_id=telefono_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        db.session.add(detalle)
        db.session.commit()
        return detalle

    def get_detalles_by_venta_id(self, venta_id):
        return DetalleVenta.query.filter_by(venta_id=venta_id).all()
