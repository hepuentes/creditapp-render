from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

# Clave secreta
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "clave-secreta")

# Configurar correctamente DATABASE_URL
DB_URL = os.environ.get("DATABASE_URL", "sqlite:///app.db")

# Solución de compatibilidad: Render puede enviar postgres:// en vez de postgresql://
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Importar rutas
from routes import auth

# Crear tablas si no existen
with app.app_context():
    db.create_all()
