from flask import Blueprint, render_template, request, redirect, url_for
from forms import AccesorioForm
from services.accesorio_service import AccesorioService

accesorio_bp = Blueprint('accesorio_bp', __name__)

@accesorio_bp.route("/accesorios_list", methods=["GET", "POST"])
def accesorios():
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
def accesorio_eliminar(id):
    accesorio_service = AccesorioService()
    accesorio_service.delete(id)
    return redirect(url_for('accesorio_bp.accesorios'))

@accesorio_bp.route("/accesorio/<id>/editar", methods=['GET', 'POST'])
def accesorio_editar(id):
    accesorio_service = AccesorioService()
    accesorio = accesorio_service.get_by_id(id)

    formulario = AccesorioForm(obj=accesorio)

    if request.method == 'POST' and formulario.validate_on_submit():
        accesorio_service.update(id, formulario.nombre.data)
        return redirect(url_for('accesorio_bp.accesorios'))

    return render_template("accesorio_edit.html", accesorio=accesorio, formulario=formulario)
