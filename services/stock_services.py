# services/stock_service.py
from repositories.stock_repositories import obtener_stock_por_telefono, actualizar_o_crear_stock

def obtener_stock_telefonos():
    return obtener_stock_por_telefono()

def agregar_stock(telefono_id, cantidad):
    stock_item = actualizar_o_crear_stock(telefono_id, cantidad)
    stock_item.cantidad += cantidad

def restar_stock(telefono_id, cantidad):
    stock_item = actualizar_o_crear_stock(telefono_id, -cantidad)
    stock_item.cantidad = max(0, stock_item.cantidad)
