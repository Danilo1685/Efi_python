from flask import Blueprint, jsonify
from models import Telefono, Accesorio, Marca, Tipo
from schemas import TelefonoSchema, AccesorioSchema, MarcaSchema, TipoSchema

main_app_bp = Blueprint('main_app_bp', __name__)

@main_app_bp.route('/main/data', methods=['GET'])
def get_all_data():
    # Obtener todos los datos de las tablas
    telefonos = Telefono.query.all()
    accesorios = Accesorio.query.all()
    marcas = Marca.query.all()
    tipos = Tipo.query.all()

    # Calcular el total del stock de teléfonos
    total_stock = 0
    for telefono in telefonos:
        # Sumar la cantidad de cada objeto Stock relacionado
        total_stock += sum(stock.cantidad for stock in telefono.stock)

    # Crear los schemas
    telefono_schema = TelefonoSchema(many=True)
    accesorio_schema = AccesorioSchema(many=True)
    marca_schema = MarcaSchema(many=True)
    tipo_schema = TipoSchema(many=True)

    # Serializar los datos
    data = {
        "telefonos": telefono_schema.dump(telefonos),
        "accesorios": accesorio_schema.dump(accesorios),
        "marcas": marca_schema.dump(marcas),
        "tipos": tipo_schema.dump(tipos),
        "total_stock_telefonos": total_stock
    }

    # Devolver la respuesta JSON
    return jsonify(data)
