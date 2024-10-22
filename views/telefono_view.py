from flask import (
    Blueprint, 
    jsonify,
    redirect, 
    render_template, 
    request, 
    url_for, 
)
from services.telefono_service import TelefonoService 
from services.telefono_service import delete_with_accesorios

from repositories.telefono_repositories import TelefonoRepositories
from schemas import (
    AccesorioSchema,
    MarcaSchema, 
    TelefonoSchema, 
    TipoSchema, 
)
from models import (
    Accesorio, 
    Marca, 
    Tipo,
) 
from forms import TelefonoForm
from app import db

telefono_bp = Blueprint('telefono', __name__)

@telefono_bp.route("/telefono_list", methods=['POST', 'GET'])
def telefonos():
    telefono_service = TelefonoService(TelefonoRepositories())
    telefonos = telefono_service.get_all()

    telefono_schema = TelefonoSchema(many=True)
    telefonos_serializados = telefono_schema.dump(telefonos)

    marcas = Marca.query.all()
    tipos = Tipo.query.all()
    accesorios = Accesorio.query.all()

    formulario = TelefonoForm()
    
    try:
        formulario.marca.choices = [(marca.id, marca.nombre) for marca in marcas]
        formulario.tipo.choices = [(tipo.id, tipo.nombre) for tipo in tipos]
        formulario.accesorio.choices = [(accesorio.id, accesorio.nombre) for accesorio in accesorios]
    except Exception as e:
        return jsonify({"error": f"Error al cargar las opciones del formulario: {str(e)}"}), 500

    if request.method == 'POST' and formulario.validate_on_submit():
        try:
            modelo = formulario.modelo.data
            anio_fabricacion = formulario.anio_fabricacion.data
            precio = formulario.precio.data
            marca = formulario.marca.data
            tipo = formulario.tipo.data
            
            telefono_service.create(modelo, anio_fabricacion, precio, marca, tipo)
            return redirect(url_for('telefono.telefonos'))
        except Exception as e:
            return jsonify({"error": f"Error al crear el teléfono: {str(e)}"}), 500

    return render_template('telefono_list.html', 
                            telefonos=telefonos_serializados, 
                            formulario=formulario, 
                            marcas=marcas, 
                            tipos=tipos, 
                            accesorios=accesorios)

@telefono_bp.route("/telefono/<id>/eliminar", methods=['POST'])
def telefono_eliminar(id):
    telefono_service = TelefonoService(TelefonoRepositories())
    telefono_service.delete_with_accesorios(id)
    return redirect(url_for('telefono.telefonos'))


@telefono_bp.route("/telefono/<id>", methods=['GET'])
def telefono_accesorio(id):
    telefono_service = TelefonoService(TelefonoRepositories())
    accesorios = telefono_service.get_accesorios_by_telefono(id)
    telefono = telefono_service.get_by_id(id)

    return render_template("accesorios_by_telefono.html", telefono=telefono, accesorios=accesorios)


@telefono_bp.route('/telefono/<int:telefono_id>', methods=['DELETE'])
def delete_telefono(telefono_id):
    try:
        delete_with_accesorios(telefono_id)
        return jsonify({"message": "Teléfono eliminado con éxito"}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500