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
            username = data.get('usuario')
            password = data.get('contrasenia')

            try:
                nuevo_usuario = Usuario(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=False,
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