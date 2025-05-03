from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

# Clave secreta (desde variable de entorno o valor por defecto)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "clave-secreta")

# ------------------------------
# 🔐 CONEXIÓN FORZADA A POSTGRESQL
# ------------------------------
try:
    DB_URL = os.environ["DATABASE_URL"]
    if DB_URL.startswith("postgres://"):
        DB_URL = DB_URL.replace("postgres://", "postgresql://")
except KeyError:
    raise RuntimeError("⚠️ La variable de entorno DATABASE_URL no está definida.")

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ------------------------------
# 🔧 Inicializar extensiones
# ------------------------------
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ------------------------------
# 🚦 Importar rutas
# ------------------------------
from routes import auth

# ------------------------------
# 🧱 Crear tablas si no existen
# ------------------------------
with app.app_context():
    db.create_all()
