import os
from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario
from schemas import UserSchema, MinimalUserSchema
from app import db 



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization
    username = data.username
    password = data.password

    usuario = Usuario.query.filter_by(username=username).first()
    
    if usuario and check_password_hash(
        pwhash=usuario.password_hash, password=password
    ):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims=dict(
                administrador=usuario.is_admin
            )
        )

        return jsonify({'Token':f'Bearer {access_token}'})

    return jsonify(Mensaje="El usuario y la contraseña al parecer no coinciden")


@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if administrador is True:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            is_admin = data.get('is_admin')


            try:
                nuevo_usuario = Usuario(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=is_admin,
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return jsonify(
                    {
                    "Mensaje":"Usuario creado correctamente",
                    "Usuario": nuevo_usuario.to_dict()
                    }
                )
            except:
                return jsonify(
                    {
                    "Mensaje":"Fallo la creacion del nuevo usuario",
                    }
                )
        else:
            return jsonify(Mensaje= "Solo el admin puede crear nuevos usuarios")
    
    usuarios = Usuario.query.all()
    if administrador is True:
        return UserSchema().dump(obj=usuarios, many=True)
    else:
        return MinimalUserSchema().dump(obj=usuarios, many=True)



@auth_bp.route('/users/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "Solo el admin puede eliminar usuarios"}), 403

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"Mensaje": "Usuario no encontrado"}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"Mensaje": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": "Fallo al eliminar el usuario", "Error": str(e)}), 500





@auth_bp.route('/users/<int:id>/update', methods=['PUT'])
@jwt_required()
def update_user(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if administrador is not True:
        return jsonify({"Mensaje": "No tienes permiso para actualizar usuarios"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin')

    try:
        user = Usuario.query.get(id)
        if not user:
            return jsonify({"Mensaje": "Usuario no encontrado"}), 404

        user.username = username if username else user.username
        user.password_hash = generate_password_hash(password) if password else user.password_hash
        user.is_admin = is_admin if is_admin is not None else user.is_admin

        db.session.commit()
        return jsonify({"Mensaje": "Usuario actualizado correctamente", "Usuario": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": "Error al actualizar el usuario: " + str(e)}), 500
