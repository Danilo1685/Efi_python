from flask import Blueprint, jsonify ,request, render_template, redirect, url_for

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from services.tipo_service import TipoService
from repositories.tipo_repositories import TipoRepositories
from schemas import TipoSchema
from forms import TipoForm
from app import db

tipo_bp = Blueprint('tipo', __name__)

@tipo_bp.route("/tipo_list", methods=['GET', 'POST'])
@jwt_required()
def tipos():
    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para crear tipos"}), 403

    tipo_service = TipoService(TipoRepositories())
    tipos = tipo_service.get_all()

    tipo_schema = TipoSchema(many=True)
    tipos_serializados = tipo_schema.dump(tipos)

    formulario = TipoForm()
    if request.method == 'POST' and formulario.validate_on_submit():
        nombre = formulario.nombre.data
        tipo_service.create(nombre)
        return redirect(url_for('tipo.tipos'))

    return render_template('tipo_list.html', tipos=tipos_serializados, formulario=formulario)

@tipo_bp.route('/tipo/<int:id>/eliminar', methods=['POST'])
@jwt_required()
def tipo_eliminar(id):
    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para borrar tipos"}), 403

    tipo_service = TipoService(TipoRepositories())
    tipo = tipo_service.get_by_id(id)
    if tipo:
        db.session.delete(tipo)
        db.session.commit()
        return redirect(url_for('tipo.tipos'))

