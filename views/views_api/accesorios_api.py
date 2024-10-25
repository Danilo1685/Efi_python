from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from forms import AccesorioForm
from services.accesorio_service import AccesorioService

accesorio_app_bp = Blueprint('accesorio_app_bp', __name__)

def accesorio_to_dict(accesorio):
    return {
        "id": accesorio.id,
        "nombre": accesorio.nombre
    }

@accesorio_app_bp.route("/api/accesorios_list", methods=["GET", "POST"])
@jwt_required()
def accesorios():

    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para crear accesorio"}), 403

    accesorio_service = AccesorioService()
    accesorios = accesorio_service.get_all()

    formulario = AccesorioForm()

    if request.method == 'POST':
        if formulario.validate_on_submit():
            nombre = formulario.nombre.data
            accesorio_service.create(nombre)
            return jsonify({"message": "Accesorio creado exitosamente"}), 201
        return jsonify({"errors": formulario.errors}), 400

    accesorios_data = [accesorio_to_dict(accesorio) for accesorio in accesorios]
    return jsonify({"accesorios": accesorios_data})

@accesorio_app_bp.route("/api/accesorio/<id>/eliminar", methods=['POST'])
@jwt_required()
def accesorio_eliminar(id):
    accesorio_service = AccesorioService()
    accesorio_service.delete(id)
    return jsonify({"message": "Accesorio eliminado exitosamente"}), 200

@accesorio_app_bp.route("/api/accesorio/<id>/editar", methods=['GET', 'POST'])
@jwt_required()
def accesorio_editar(id):

    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para editar accesorio"}), 403

    accesorio_service = AccesorioService()
    accesorio = accesorio_service.get_by_id(id)

    formulario = AccesorioForm(obj=accesorio)

    if request.method == 'POST' and formulario.validate_on_submit():
        accesorio_service.update(id, formulario.nombre.data)
        return jsonify({"message": "Accesorio actualizado exitosamente"}), 200

    accesorio_data = accesorio_to_dict(accesorio)
    return jsonify({"accesorio": accesorio_data})
