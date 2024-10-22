import os
from datetime import timedelta
from flask_cors import CORS

# Imports de Flask
from flask import ( 
    Flask, 
    flash, 
    jsonify, 
    redirect, 
    render_template, 
    request, 
    url_for, 
)

# Imports de Werkzeug security 
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash,
)

# Imports de Flask JWT 
from flask_jwt_extended import (
    JWTManager,
    create_access_token, 
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

#Imports de SQLAlchemy, Marshmallow, Migrate 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__) 
cors = CORS(app,resources={r"/*" : {"origins": "*"}})
#Configuracion
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Inicializa las extenciones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
jwt = JWTManager(app)

from views import register_blueprint

# Registro de blueprints
register_blueprint(app)


@app.route("/")
def index():
    return render_template('index.html')

