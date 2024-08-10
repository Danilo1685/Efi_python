from app import db

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