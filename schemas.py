from marshmallow import fields
from app import ma
from models import (Accesorio, 
    Cliente, 
    DetalleVenta,
    Marca,  
    Telefono_Accesorio, 
    Telefono, 
    Tipo, 
    Stock, 
    Usuario, 
    Venta,
    
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

class VentaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Venta
        load_instance = True  
        include_fk = True 

    id = ma.auto_field()  
    cliente_id = ma.auto_field()  
    total = ma.auto_field()
    
    cliente = ma.Nested('ClienteSchema', many=False)
    
    detalles = ma.Nested('DetalleVentaSchema', many=True)


class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente
        load_instance = True

    id = ma.auto_field()
    nombre = ma.auto_field()


class DetalleVentaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DetalleVenta
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    venta_id = ma.auto_field()
    telefono_id = ma.auto_field()
    cantidad = ma.auto_field()
    precio_unitario = ma.auto_field()

    telefono = ma.Nested('TelefonoSchema', many=False)


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