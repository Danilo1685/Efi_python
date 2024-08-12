from flask import Flask, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) 

# Configuracion de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import  Accesorio, Cliente, DetalleVenta, Marca,  Telefono_Accesorio, Telefono , Tipo, Stock, Venta

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/marca_list", methods=['POST', 'GET'])
def marcas():   
    marcas = Marca.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template('marca_list.html',
                marcas=marcas)

@app.route("/marca/<id>/telefono")
def telefonos_por_marca(id):
    marca = Marca.query.get_or_404(id)
    telefonos = marca.telefonos
    return render_template("telefonos_by_marca.html", telefonos=telefonos, marca=marca)


@app.route("/marca/<id>/editar", methods=['GET', 'POST'])
def marca_editar(id):
    marca = Marca.query.get_or_404(id)

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template("marca_edit.html", marca=marca)


@app.route("/marca/<id>/eliminar", methods=['POST'])
def marca_eliminar(id):
    marca = Marca.query.get_or_404(id)
    if marca.telefonos:
        for telefono in marca.telefonos:
            db.session.delete(telefono)
    
    db.session.delete(marca)
    db.session.commit()
    return redirect(url_for('marcas'))

@app.route("/tipo_list", methods=['GET', 'POST'])
def tipos():
    tipos = Tipo.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nuevo_tipo = Tipo(nombre=nombre)
        db.session.add(nuevo_tipo)
        db.session.commit()
        return redirect(url_for('tipos'))

    return render_template('tipo_list.html', tipos=tipos)
@app.route("/tipo/<id>/eliminar", methods=['POST'])
def tipo_eliminar(id):
    tipo = Tipo.query.get_or_404(id)
    if tipo.telefonos:
        for telefono in tipo.telefonos:
            db.session.delete(telefono)

    db.session.delete(tipo)
    db.session.commit()
    return redirect(url_for('tipos'))


@app.route("/telefono_list", methods=['POST', 'GET'])
def telefonos():
    telefonos = Telefono.query.all()
    accesorios = Accesorio.query.all()
    marcas = Marca.query.all()
    tipos = Tipo.query.all()

    if request.method == 'POST':
        modelo = request.form['modelo']
        anio = request.form['anio_fabricacion']
        precio = request.form['precio']
        accesorio = request.form['accesorio']
        marca = request.form['marca']
        tipo = request.form['tipo']
        telefono_nuevo = Telefono(
            modelo=modelo,
            anio_fabricacion=anio,
            precio=precio,
            marca_id=marca,
            tipo_id=tipo,
        )
        db.session.add(telefono_nuevo)
        db.session.commit()
        return redirect(url_for('telefonos'))

    return render_template('telefono_list.html', telefonos=telefonos, accesorios=accesorios, marcas=marcas, tipos=tipos)

@app.route("/telefono/<id>/eliminar", methods=['POST'])
def telefono_eliminar(id):
    telefono = Telefono.query.get_or_404(id)
    for stock in telefono.stocks:
        stock.cantidad -= 1
        if stock.cantidad <= 0:
            db.session.delete(stock)
    
    for accesorio in telefono.accesorios:
        db.session.delete(accesorio)
    db.session.delete(telefono)
    db.session.commit()
    return redirect(url_for('telefonos'))



@app.route("/accesorios_list", methods=["GET", "POST"])
def accesorios():
    accesorios = Accesorio.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nuevo_accesorio = Accesorio(nombre=nombre)
        db.session.add(nuevo_accesorio)
        db.session.commit()
        return redirect(url_for('accesorios'))

    return render_template('accesorios_list.html', accesorios=accesorios)

@app.route("/telefono/<id>", methods=['GET'])
def telefono_accesorio(id):
    telefono = Telefono.query.get_or_404(id)
    accesorios = [ta.accesorio for ta in Telefono_Accesorio.query.filter_by(telefono_id=id).all()]
    return render_template("accesorios_by_telefono.html", telefono=telefono, accesorios=accesorios)

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

