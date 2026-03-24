from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database import get_usuarios, crear_usuario, eliminar_usuario
from functools import wraps

bp = Blueprint('usuarios', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))
        if session['usuario']['rol'] != 'admin':
            return redirect(url_for('pos.index'))
        return f(*args, **kwargs)
    return decorated

@bp.route('/usuarios')
@admin_required
def index():
    usuarios = get_usuarios()
    return render_template('usuarios.html', usuarios=usuarios, usuario=session['usuario'])

@bp.route('/usuarios/crear', methods=['POST'])
@admin_required
def crear():
    data = request.get_json()
    try:
        crear_usuario(data['nombre'], data['password'], data['rol'])
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'msg': 'El nombre de usuario ya existe.'})

@bp.route('/usuarios/eliminar/<int:user_id>', methods=['POST'])
@admin_required
def eliminar(user_id):
    eliminar_usuario(user_id)
    return jsonify({'ok': True})