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

# Ruta de login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization
    if not data:
        return jsonify({"Mensaje": "Faltan las credenciales"}), 400

    username = data.username
    password = data.password

    usuario = Usuario.query.filter_by(username=username).first()

    if usuario and check_password_hash(pwhash=usuario.password_hash, password=password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims=dict(is_admin=usuario.is_admin)
        )
        return jsonify({"Token": access_token}), 200

    return jsonify({"Mensaje": "La contraseña no coincide o el usuario no existe"}), 401

@auth_bp.route('/users', methods=['POST', 'GET'])
@jwt_required()
def users():
    additional_info = get_jwt()
    current_user = get_jwt_identity()
    is_admin = additional_info.get('is_admin')

    if request.method == 'POST':
        if not is_admin:
            return jsonify({"Mensaje": "No está autorizado para crear usuarios"}), 403

        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"Mensaje": "Datos incompletos"}), 400

        username = data.get('username')
        password = data.get('password')

        password_encrypted = generate_password_hash(
            password=password,
            method="pbkdf2",
            salt_length=8,
        )

        try:
            nuevo_usuario = Usuario(
                username=username,
                password_hash=password_encrypted,
                is_admin=False, 

            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return jsonify({"Usuario creado": nuevo_usuario.username}), 201
        except Exception as e:
            return jsonify({"Error": "Hubo un error al crear el usuario", "Detalle": str(e)}), 500

    usuarios = Usuario.query.all()

    if is_admin:
        return jsonify(UserSchema().dump(usuarios, many=True)), 200

    return jsonify(MinimalUserSchema().dump(usuarios, many=True)), 200
