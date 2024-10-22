from flask import Blueprint, request, render_template, redirect, url_for
from app import db
from services.marca_service import MarcaService
from repositories.marca_repositories import MarcaRepositories
from schemas import MarcaSchema, TelefonoSchema
from models import Marca
from forms import MarcaForm

marca_bp = Blueprint('marca', __name__)

@marca_bp.route("/marca_list", methods=['POST', 'GET'])
def marcas():  
    marca_service = MarcaService(MarcaRepositories())
    marcas = marca_service.get_all()

    marca_schema = MarcaSchema(many=True)
    marcas_serializadas = marca_schema.dump(marcas)

    formulario = MarcaForm()
    if request.method == 'POST':
        nombre = formulario.nombre.data
        marca_service.create(nombre)
        return redirect(url_for('marca.marcas'))

    return render_template('marca_list.html', marcas=marcas_serializadas, formulario=formulario)

@marca_bp.route("/marca/<id>/telefono")
def telefonos_por_marca(id):
    marca_service = MarcaService(MarcaRepositories())
    telefonos = marca_service.get_telefonos_por_marca(id)
    marca = marca_service.get_by_id(id)

    telefono_schema = TelefonoSchema(many=True)
    marca_schema = MarcaSchema()

    telefonos_serializados = telefono_schema.dump(telefonos)
    marca_serializada = marca_schema.dump(marca)

    return render_template("telefonos_by_marca.html", telefonos=telefonos_serializados, marca=marca_serializada)

@marca_bp.route("/marca/<id>/editar", methods=['GET', 'POST'])
def marca_editar(id):
    marca = Marca.query.get_or_404(id)

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marca.marcas'))

    return render_template("marca_edit.html", marca=marca)
