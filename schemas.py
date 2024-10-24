from marshmallow import fields
from app import ma
from models import (Accesorio, 
    Marca,  
    Telefono_Accesorio, 
    Telefono, 
    Tipo, 
    Stock, 
    Usuario,    
)


class UserSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = Usuario

    id = ma.auto_field()
    username = ma.auto_field()   
    is_admin = ma.auto_field()
    password_hash = ma.auto_field()

class MinimalUserSchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = Usuario

    username = ma.auto_field()   


class TelefonoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Telefono

    id = ma.auto_field()
    modelo = ma.auto_field()
    anio_fabricacion = ma.auto_field()
    precio = ma.auto_field()
    marca = ma.Nested('MarcaSchema')
    tipo = ma.Nested('TipoSchema')

class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    id = ma.auto_field()
    nombre = ma.auto_field()

class TipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tipo

    id = ma.auto_field()
    nombre = ma.auto_field()

class TelefonoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Telefono
        include_fk = True  

    id = ma.auto_field()  
    modelo = ma.auto_field()
    anio_fabricacion = ma.auto_field()
    precio = ma.auto_field()

    marca = fields.Nested('MarcaSchema')  
    tipo = fields.Nested('TipoSchema')  


class StockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stock  

    telefono_id = ma.auto_field()
    cantidad = ma.auto_field()


class AccesorioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio

    id = ma.auto_field()
    nombre = ma.auto_field()