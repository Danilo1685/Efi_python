from flask import Blueprint, request, jsonify, redirect, url_for

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app import db
from services.marca_service import MarcaService
from repositories.marca_repositories import MarcaRepositories
from schemas import MarcaSchema, TelefonoSchema
from models import Marca
from forms import MarcaForm

marca_app_bp = Blueprint('marca_app_bp', __name__)

@marca_app_bp.route("/api/marca_list", methods=['POST', 'GET'])
@jwt_required()
def marcas(): 

    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para crear marcas"}), 403

    marca_service = MarcaService(MarcaRepositories())
    marcas = marca_service.get_all()

    marca_schema = MarcaSchema(many=True)
    marcas_serializadas = marca_schema.dump(marcas)

    formulario = MarcaForm()
    if request.method == 'POST':
        nombre = formulario.nombre.data
        marca_service.create(nombre)
        return redirect(url_for('marca.marcas'))

    return jsonify({'marcas': marcas_serializadas})


@marca_app_bp.route("/api/marca/<id>/telefono")
@jwt_required()
def telefonos_por_marca(id):
    marca_service = MarcaService(MarcaRepositories())
    telefonos = marca_service.get_telefonos_por_marca(id)
    marca = marca_service.get_by_id(id)

    telefono_schema = TelefonoSchema(many=True)
    marca_schema = MarcaSchema()

    telefonos_serializados = telefono_schema.dump(telefonos)
    marca_serializada = marca_schema.dump(marca)

    return jsonify({
        'telefonos': telefonos_serializados,
        'marca': marca_serializada
    })


@marca_app_bp.route("/api/marca/<id>/editar", methods=['GET', 'POST'])
@jwt_required()
def marca_editar(id):


    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para editar marca"}), 403

    marca = Marca.query.get_or_404(id)

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marca.marcas'))

    marca_schema = MarcaSchema()
    marca_serializada = marca_schema.dump(marca)

    return jsonify({'marca': marca_serializada})
