# repositories/stock_repository.py
from app import db
from models import Stock

def obtener_stock_por_telefono():
    return Stock.query.all()

def actualizar_o_crear_stock(telefono_id, cantidad):
    stock_item = Stock.query.filter_by(telefono_id=telefono_id).with_for_update().first()
    if stock_item:
        return stock_item
    else:
        nuevo_stock = Stock(telefono_id=telefono_id, cantidad=cantidad)
        db.session.add(nuevo_stock)
        db.session.commit()
        return nuevo_stock
