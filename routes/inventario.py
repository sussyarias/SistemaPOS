from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database import get_productos, get_categorias, crear_producto, editar_producto, eliminar_producto, get_productos_stock_bajo
from functools import wraps

bp = Blueprint('inventario', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@bp.route('/inventario')
@login_required
def index():
    productos  = get_productos()
    categorias = get_categorias()
    stock_bajo = get_productos_stock_bajo()
    return render_template('inventario.html', productos=productos, categorias=categorias, stock_bajo=stock_bajo, usuario=session['usuario'])

@bp.route('/inventario/crear', methods=['POST'])
@login_required
def crear():
    data = request.get_json()
    crear_producto(data['nombre'], data['precio'], data['stock'], data['stock_minimo'], data['categoria_id'])
    return jsonify({'ok': True})

@bp.route('/inventario/editar/<int:prod_id>', methods=['POST'])
@login_required
def editar(prod_id):
    data = request.get_json()
    editar_producto(prod_id, data['nombre'], data['precio'], data['stock'], data['stock_minimo'], data['categoria_id'])
    return jsonify({'ok': True})

@bp.route('/inventario/eliminar/<int:prod_id>', methods=['POST'])
@login_required
def eliminar(prod_id):
    eliminar_producto(prod_id)
    return jsonify({'ok': True})
