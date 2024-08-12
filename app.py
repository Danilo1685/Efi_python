from flask import Flask, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) 

# Configuracion de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Marca, Tipo, Telefono, Accesorio, Telefono_Accesorio , Stock

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

    # Opcional: si hay teléfonos asociados a esta marca, podrías querer manejar esa relación aquí
    if marca.telefonos:
        # Por ejemplo, podrías querer eliminar todos los teléfonos asociados antes de eliminar la marca
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

    # Manejar relaciones si es necesario
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
    
    # Si tienes relaciones con accesorios, asegúrate de eliminarlas o actualizarlas también
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

    # Eliminar las relaciones con teléfonos
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

        # Verificar si ya existe un registro de stock para ese teléfono
        stock_item = Stock.query.filter_by(telefono_id=telefono_id).with_for_update().first()
        if stock_item:
            stock_item.cantidad += cantidad  # Actualizar stock existente
        else:
            nuevo_stock = Stock(telefono_id=telefono_id, cantidad=cantidad)  # Crear nuevo registro
            db.session.add(nuevo_stock)
        
        db.session.commit()
        return redirect(url_for('stock'))

    # Enviar a la plantilla la información de cada teléfono junto con su cantidad de stock
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

    # Buscar el stock del teléfono con bloqueo
    stock_item = Stock.query.filter_by(telefono_id=telefono_id).with_for_update().first()

    if stock_item:
        # Restar la cantidad indicada
        stock_item.cantidad -= cantidad
        # Asegurarse de que el stock no sea negativo
        if stock_item.cantidad < 0:
            stock_item.cantidad = 0
        db.session.commit()

    return redirect(url_for('stock'))
