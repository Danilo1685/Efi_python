from flask import Blueprint, request, render_template, redirect, url_for
from services.tipo_service import TipoService
from repositories.tipo_repositories import TipoRepositories
from schemas import TipoSchema
from forms import TipoForm
from app import db

tipo_bp = Blueprint('tipo', __name__)

@tipo_bp.route("/tipo_list", methods=['GET', 'POST'])
def tipos():
    tipo_service = TipoService(TipoRepositories())
    tipos = tipo_service.get_all()

    # Usar el esquema para serializar los tipos
    tipo_schema = TipoSchema(many=True)
    tipos_serializados = tipo_schema.dump(tipos)

    formulario = TipoForm()
    if request.method == 'POST':
        nombre = formulario.nombre.data
        tipo_service.create(nombre)
        return redirect(url_for('tipo.tipos'))

    return render_template('tipo_list.html', tipos=tipos_serializados, formulario=formulario)

@tipo_bp.route("/tipo/<id>/eliminar", methods=['POST'])
def tipo_eliminar(id):
    tipo_service = TipoService(TipoRepositories())
    tipo = tipo_service.get_by_id(id)

    if tipo.telefonos:
        tipo_service.delete_with_telefonos(tipo)

    return redirect(url_for('tipo.tipos'))
