from flask import Blueprint, request, redirect, url_for, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from services.stock_services import obtener_stock_telefonos, agregar_stock, restar_stock
from forms import TelefonoCantidadForm
from app import db
from models import Stock, Telefono

stock_app_bp = Blueprint('stock_app_bp', __name__)

@stock_app_bp.route("/api/stock", methods=['GET', 'POST'])
@jwt_required()
def stock():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')  

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para acceder a esta ruta"}), 403

    telefonos = Telefono.query.all()

    if request.method == 'POST':
        telefono_id = request.form.get('telefono_id')
        cantidad = request.form.get('cantidad')

        if telefono_id is None or cantidad is None:
            return jsonify({"Mensaje": "Debe proporcionar 'telefono_id' y 'cantidad'"}), 400

        try:
            cantidad = int(cantidad)
        except ValueError:
            return jsonify({"Mensaje": "Cantidad debe ser un número entero"}), 400

        stock_item = Stock.query.filter_by(telefono_id=telefono_id).with_for_update().first()
        if stock_item:
            stock_item.cantidad += cantidad
        else:
            nuevo_stock = Stock(telefono_id=telefono_id, cantidad=cantidad)
            db.session.add(nuevo_stock)
        
        db.session.commit()
        return redirect(url_for('stock_app_bp.stock'))

    telefonos_con_stock = [
        {
            'telefono': telefono.modelo,  
            'stock': Stock.query.filter_by(telefono_id=telefono.id).first().cantidad if Stock.query.filter_by(telefono_id=telefono.id).first() else 0
        }
        for telefono in telefonos
    ]

    return jsonify(telefonos_con_stock)


@stock_app_bp.route("/api/restar_stock", methods=['POST'])
@jwt_required()
def restar_stock_view():
    additional_info = get_jwt()
    administrador = additional_info.get('administrador') 

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para borrar stock"}), 403

    form = TelefonoCantidadForm()
    if form.validate_on_submit():
        restar_stock(form.telefono.data, form.cantidad.data)
        return jsonify({"Mensaje": "Stock restado correctamente"}), 200
    return jsonify({"Mensaje": "Datos inválidos"}), 400