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
    

    #Relacion directa con el otro objeto
    marca = db.relationship('Marca', backref=db.backref('telefono', lazy=True))
    tipo = db.relationship('Tipo', backref=db.backref('telefono', lazy=True))
    accesorios = db.relationship('Telefono_Accesorio', backref=db.backref('telefono',lazy=True))
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