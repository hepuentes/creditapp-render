from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

@auth_bp.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for('auth.index'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/crear-admin')
def crear_admin():
    if Usuario.query.filter_by(username='admin').first():
        return 'El usuario admin ya existe.'
    
    admin = Usuario(
        nombre="Admin",
        username="admin",
        email="admin@email.com",
        rol="administrador"
    )
    admin.set_password("123456")
    db.session.add(admin)
    db.session.commit()
    return 'Usuario administrador creado. Puedes iniciar sesión en /login'
