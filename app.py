from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Carga variables de entorno (.env o Render)
load_dotenv()

app = Flask(__name__)

# Clave secreta para sesiones
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-super-secreta')

# Configura la base de datos desde DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importa modelos y rutas
from models.usuario import Usuario
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

# Crea las tablas si no existen (solo la primera vez)
with app.app_context():
    db.create_all()

# Página protegida (dashboard)
@app.route('/')
def index():
    return 'App funcionando correctamente. Inicia sesión en /login'

if __name__ == '__main__':
    app.run()
