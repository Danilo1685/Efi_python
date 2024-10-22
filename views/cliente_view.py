# views/cliente_view.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from services.cliente_service import ClienteService
from models import Cliente, Venta
from forms import ClienteForm

cliente_bp = Blueprint('cliente', __name__)

cliente_service = ClienteService() 

@cliente_bp.route("/cliente_list", methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        datos = {
            'nombre': form.nombre.data,
            'correo': form.correo.data,
            'telefono': form.telefono.data,
            'direccion': form.direccion.data
        }
        cliente_service.crear_cliente(datos)
        flash('Cliente creado correctamente.', 'success')
        return redirect(url_for('cliente.clientes'))  
    
    clientes = cliente_service.obtener_todos_los_clientes()
    return render_template('cliente_list.html', clientes=clientes, form=form)


@cliente_bp.route("/cliente/<id>/editar", methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = cliente_service.obtener_cliente_por_id(id)
    form = ClienteForm(obj=cliente)
    
    if form.validate_on_submit():
        datos = {
            'nombre': form.nombre.data,
            'correo': form.correo.data,
            'telefono': form.telefono.data,
            'direccion': form.direccion.data
        }
        cliente_service.actualizar_cliente(id, datos)
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('cliente.clientes'))

    return render_template("cliente_edit.html", form=form)


@cliente_bp.route('/cliente/<int:cliente_id>/eliminar', methods=['POST'])
def cliente_eliminar(cliente_id):
    cliente = cliente_service.obtener_cliente_por_id(cliente_id)
    if cliente is None:
        flash('Cliente no encontrado.', 'error')
        return redirect(url_for('cliente.clientes'))  
    
    default_cliente_id = 1 
    ventas = Venta.query.filter_by(cliente_id=cliente_id).all()
    for venta in ventas:
        venta.cliente_id = default_cliente_id  
    db.session.commit() 
    db.session.delete(cliente)
    db.session.commit() 

    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('cliente.clientes'))  