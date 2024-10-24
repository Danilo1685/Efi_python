from app import db
from datetime import datetime

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.nombre

class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f"Tipo {self.nombre}"

class Telefono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50), nullable=False)
    anio_fabricacion = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)

    marca = db.relationship('Marca', backref=db.backref('telefonos', lazy=True))
    tipo = db.relationship('Tipo', backref=db.backref('telefonos', lazy=True))
    stock = db.relationship('Stock', back_populates='telefono_relacion', lazy=True, overlaps='stocks,telefono_relacion')
    accesorios = db.relationship('Telefono_Accesorio', backref='telefono', lazy=True, overlaps='accesorios,telefonos')
    
    def __str__(self):
        return f"Telefono {self.modelo}"

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    telefonos = db.relationship('Telefono_Accesorio', back_populates='accesorio', lazy=True)

    def __str__(self):
        return self.nombre


class Telefono_Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono_id = db.Column(db.Integer, db.ForeignKey('telefono.id'), nullable=False)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), nullable=False)

    accesorio = db.relationship('Accesorio', back_populates='telefonos')

    def __str__(self):
        return f"Accesorio {self.accesorio.nombre} para el teléfono {self.telefono.modelo}"
    

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono_id = db.Column(db.Integer, db.ForeignKey('telefono.id'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    telefono_relacion = db.relationship('Telefono', back_populates='stock', lazy=True, overlaps='stock,telefono_relacion')

    def __str__(self):
        return f"Stock: {self.cantidad} unidades de {self.telefono_relacion.modelo}"

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def __str__(self):
        return self.username
