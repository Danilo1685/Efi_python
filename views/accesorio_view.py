from flask import Blueprint, jsonify,render_template, request, redirect, url_for

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from forms import AccesorioForm
from services.accesorio_service import AccesorioService

accesorio_bp = Blueprint('accesorio_bp', __name__)

@accesorio_bp.route("/accesorios_list", methods=["GET", "POST"])
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
            return redirect(url_for('accesorio_bp.accesorios'))
        # Si no es válido, renderiza el formulario con los errores
        return render_template('accesorios_list.html', accesorios=accesorios, formulario=formulario)

    return render_template('accesorios_list.html', accesorios=accesorios, formulario=formulario)

@accesorio_bp.route("/accesorio/<id>/eliminar", methods=['POST'])
@jwt_required()
def accesorio_eliminar(id):

    additional_info = get_jwt()
    is_admin = additional_info.get('is_admin')

    if not is_admin:  
        return jsonify({"Mensaje": "No está autorizado para eliminar accesorio"}), 403

    accesorio_service = AccesorioService()
    accesorio_service.delete(id)
    return redirect(url_for('accesorio_bp.accesorios'))

@accesorio_bp.route("/accesorio/<id>/editar", methods=['GET', 'POST'])
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
        return redirect(url_for('accesorio_bp.accesorios'))

    return render_template("accesorio_edit.html", accesorio=accesorio, formulario=formulario)
