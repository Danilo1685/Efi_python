from flask import Blueprint, render_template, redirect, url_for, request
from forms import VentaForm
from services.venta_service import VentaService
from schemas import VentaSchema, DetalleVentaSchema 

ventas_bp = Blueprint('ventas', __name__)
venta_service = VentaService()

venta_schema = VentaSchema(many=True)  
detalle_venta_schema = DetalleVentaSchema(many=True)  
single_venta_schema = VentaSchema()  
@ventas_bp.route("/venta_list", methods=['GET', 'POST'])
def ventas():
    if request.method == 'POST':
        form = VentaForm()
        if form.validate_on_submit():
            cliente_id = form.cliente_id.data
            total = form.total.data
            venta_service.agregar_venta(cliente_id, total)
            return redirect(url_for('ventas.ventas'))

    ventas = venta_service.obtener_ventas()  
    ventas_serializadas = venta_schema.dump(ventas) 
    return render_template('venta_list.html', ventas=ventas_serializadas)

@ventas_bp.route("/venta/<int:id>/detalle", methods=['GET', 'POST'])
def detalle_venta(id):
    venta = venta_service.obtener_venta_by_id(id)  
    venta_serializada = single_venta_schema.dump(venta)  

    if request.method == 'POST':
        telefono_id = request.form['telefono_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']

        # Agregamos el detalle de la venta
        venta_service.agregar_detalle(id, telefono_id, cantidad, precio_unitario)
        venta_service.actualizar_total_venta(venta, cantidad, precio_unitario)

        return redirect(url_for('ventas.detalle_venta', id=id))

    detalles = venta_service.get_detalles_by_venta_id(id) 
    detalles_serializados = detalle_venta_schema.dump(detalles)  
    return render_template('detalle_venta.html', venta=venta_serializada, detalles=detalles_serializados)
