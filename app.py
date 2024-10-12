import os
from datetime import timedelta

# Flask imports
from flask import ( 
    Flask, 
    flash, 
    jsonify, 
    redirect, 
    render_template, 
    request, 
    url_for,
)

# Werkzeug security imports
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash,
)

# Flask JWT imports
from flask_jwt_extended import (
    JWTManager,
    create_access_token, 
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

# SQLAlchemy, Marshmallow, Migrate imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# Environment variables
from dotenv import load_dotenv



# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__) 

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Local imports
from models import (
    Accesorio, 
    Cliente, 
    DetalleVenta,
    Telefono_Accesorio, 
    Telefono, 
    Stock, 
    Venta,
)
from forms import AccesorioForm
from services.accesorio_service import AccesorioService
from repositories.accesorio_repositories import AccesorioRepositories

from views import register_blueprint

# Register blueprints
register_blueprint(app)




@app.route("/")
def index():
    return render_template('index.html')


@app.route("/accesorios_list", methods=["GET", "POST"])
def accesorios():
    accesorio_service = AccesorioService(AccesorioRepositories())
    accesorios = accesorio_service.get_all()

    formulario = AccesorioForm()

    if request.method == 'POST':
        nombre = formulario.nombre.data
        accesorio_service.create(nombre)
        return redirect(url_for('accesorios'))

    return render_template('accesorios_list.html', accesorios=accesorios, formulario=formulario)

@app.route("/accesorio/<id>/eliminar", methods=['POST'])
def accesorio_eliminar(id):
    accesorio = Accesorio.query.get_or_404(id)
    Telefono_Accesorio.query.filter_by(accesorio_id=id).delete()
    
    db.session.delete(accesorio)
    db.session.commit()
    return redirect(url_for('accesorios'))

@app.route("/accesorio/<id>/editar", methods=['GET', 'POST'])
def accesorio_editar(id):
    accesorio = Accesorio.query.get_or_404(id)

    if request.method == 'POST':
        accesorio.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('accesorios'))

    return render_template("accesorio_edit.html", accesorio=accesorio)




@app.route("/stock", methods=['GET', 'POST'])
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
        return redirect(url_for('stock'))

    telefonos_con_stock = []
    for telefono in telefonos:
        stock_item = Stock.query.filter_by(telefono_id=telefono.id).first()
        telefonos_con_stock.append({
            'telefono': telefono,
            'stock': stock_item.cantidad if stock_item else 0
        })

    return render_template('stock.html', telefonos=telefonos_con_stock)

@app.route("/restar_stock", methods=['POST'])
def restar_stock():
    telefono_id = request.form['telefono_id']
    cantidad = int(request.form['cantidad'])
    stock_item = Stock.query.filter_by(telefono_id=telefono_id).with_for_update().first()

    if stock_item:
        stock_item.cantidad -= cantidad
        if stock_item.cantidad < 0:
            stock_item.cantidad = 0
        db.session.commit()

    return redirect(url_for('stock'))



@app.route("/cliente_list", methods=['GET', 'POST'])
def clientes():
    clientes = Cliente.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')

        nuevo_cliente = Cliente(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('clientes'))

    return render_template('cliente_list.html', clientes=clientes)

@app.route("/cliente/<id>/editar", methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.correo = request.form['correo']
        cliente.telefono = request.form.get('telefono')
        cliente.direccion = request.form.get('direccion')

        db.session.commit()
        return redirect(url_for('clientes'))

    return render_template("cliente_edit.html", cliente=cliente)

@app.route("/cliente/<id>/eliminar", methods=['POST'])
def cliente_eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes'))




@app.route("/venta_list", methods=['GET', 'POST'])
def ventas():
    ventas = Venta.query.all()
    clientes = Cliente.query.all()

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        total = request.form['total']

        nueva_venta = Venta(cliente_id=cliente_id, total=total)
        db.session.add(nueva_venta)
        db.session.commit()
        return redirect(url_for('ventas'))

    return render_template('venta_list.html', ventas=ventas, clientes=clientes)

@app.route("/venta/<id>/detalle", methods=['GET', 'POST'])
def detalle_venta(id):
    venta = Venta.query.get_or_404(id)
    telefonos = Telefono.query.all()

    if request.method == 'POST':
        telefono_id = request.form['telefono_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']

        detalle = DetalleVenta(
            venta_id=id,
            telefono_id=telefono_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        db.session.add(detalle)
        db.session.commit()
        
        # Actualizar el total de la venta
        venta.total += int(cantidad) * int(precio_unitario)
        db.session.commit()

        return redirect(url_for('detalle_venta', id=id))

    detalles = DetalleVenta.query.filter_by(venta_id=id).all()
    return render_template('detalle_venta.html', venta=venta, telefonos=telefonos, detalles=detalles)

