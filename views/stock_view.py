from flask import Blueprint, jsonify, render_template, request, redirect, url_for

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

stock_bp = Blueprint('stock', __name__)

@stock_bp.route("/stock", methods=['GET', 'POST'])
@jwt_required()
def stock():
    additional_info = get_jwt()
    administrador = additional_info.get('administrador')

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para agregar stock"}), 403

    telefonos = Telefono.query.all()

    if request.method == 'POST':
        telefono_id = request.form['telefono_id']
        cantidad = int(request.form['cantidad'])
        stock_item = Stock.query.filter_by(telefono_id=telefono_id).with_for_update().first()
        if stock_item:
            stock_item.cantidad += cantidad  
        else:
            nuevo_stock = Stock(telefono_id=telefono_id, cantidad=cantidad)  
            db.session.add(nuevo_stock)
        
        db.session.commit()
        return redirect(url_for('stock.stock'))

    telefonos_con_stock = []
    for telefono in telefonos:
        stock_item = Stock.query.filter_by(telefono_id=telefono.id).first()
        telefonos_con_stock.append({
            'telefono': telefono,
            'stock': stock_item.cantidad if stock_item else 0
        })

    return render_template('stock.html', telefonos=telefonos_con_stock)

@stock_bp.route("/restar_stock", methods=['POST'])
@jwt_required()
def restar_stock_view():
    additional_info = get_jwt()
    administrador = additional_info.get('administrador')

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para borrar stock"}), 403

    form = TelefonoCantidadForm()
    if form.validate_on_submit():
        restar_stock(form.telefono.data, form.cantidad.data)
        return redirect(url_for('stock.stock'))
    
    return jsonify({"Mensaje": "Error al restar stock"}), 400
