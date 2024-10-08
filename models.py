from app import db
from datetime import datetime
class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre

class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return f"Tipo {self.nombre}"


class Telefono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50), nullable=False)
    anio_fabricacion = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)
    

    # Relación directa con el otro objeto
    marca = db.relationship('Marca', backref=db.backref('telefonos', lazy=True))
    tipo = db.relationship('Tipo', backref=db.backref('telefonos', lazy=True))
    stock = db.relationship('Stock', backref='telefono_relacion', lazy=True)  # Cambiado el nombre del backref aquí
    accesorios = db.relationship('Telefono_Accesorio', backref='telefono', lazy=True)
    
    def __str__(self) -> str:
        return f"Telefono {self.modelo}"
    

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefonos = db.relationship('Telefono_Accesorio', backref=db.backref ('accesorios', lazy=True))

    def __str__(self) -> str:
        return self.nombre

class Telefono_Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono_id = db.Column(db.Integer, db.ForeignKey('telefono.id'), nullable=False)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), nullable=False)

    accesorio = db.relationship('Accesorio', backref=db.backref ('telefono_accesorio', lazy=True))

    def __str__(self) -> str:
        return f"Accesorio {self.accesorio.nombre} para el telefono {self.telefono.modelo}"
    

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono_id = db.Column(db.Integer, db.ForeignKey('telefono.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    telefono = db.relationship('Telefono', backref=db.backref('stocks', lazy=True))  # Cambiado el nombre del backref aquí

    def __str__(self) -> str:
        return f"Stock: {self.cantidad} unidades de {self.telefono.modelo}"
    

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.correo})"
    

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Integer, nullable=False, default=0)

    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

    def __str__(self) -> str:
        return f"Venta #{self.id} - Cliente: {self.cliente.nombre} - Fecha: {self.fecha.strftime('%Y-%m-%d')} - Total: {self.total}"

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    telefono_id = db.Column(db.Integer, db.ForeignKey('telefono.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Integer, nullable=False)

    telefono = db.relationship('Telefono', backref=db.backref('detalles_venta', lazy=True))

    def __str__(self) -> str:
        return f"Detalle Venta - Teléfono: {self.telefono.modelo} - Cantidad: {self.cantidad} - Precio Unitario: {self.precio_unitario}"



