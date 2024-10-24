from flask import Blueprint, request, redirect, url_for, jsonify
from services.stock_services import obtener_stock_telefonos, agregar_stock, restar_stock
from forms import TelefonoCantidadForm
from app import db
from models import Stock, Telefono

stock_app_bp = Blueprint('stock_app_bp', __name__)

@stock_app_bp.route("/api/stock", methods=['GET', 'POST'])
def stock():
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
            'telefono': telefono.modelo,  # Asegúrate de que 'modelo' sea un atributo válido
            'stock': stock_item.cantidad if stock_item else 0
        })

    return jsonify(telefonos_con_stock)

@stock_app_bp.route("/api/restar_stock", methods=['POST'])
def restar_stock_view():
    form = TelefonoCantidadForm()
    if form.validate_on_submit():
        restar_stock(form.telefono.data, form.cantidad.data)
    return redirect(url_for('stock.stock'))
