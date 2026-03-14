from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from database import get_productos, get_categorias, crear_factura
from printer import imprimir_factura
from datetime import datetime
from functools import wraps

bp = Blueprint('pos', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@bp.route('/pos')
@login_required
def index():
    productos  = get_productos()
    categorias = get_categorias()
    return render_template('pos.html', productos=productos, categorias=categorias, usuario=session['usuario'])

@bp.route('/pos/facturar', methods=['POST'])
@login_required
def facturar():
    data      = request.get_json()
    items     = data.get('items', [])
    descuento = float(data.get('descuento', 0))
    cajero    = session['usuario']['nombre']
    subtotal  = sum(i['cant'] * i['precio'] for i in items)
    base      = max(subtotal - descuento, 0)
    iva       = round(base * 0.13)
    total     = base + iva
    fecha     = datetime.now().strftime('%d/%m/%Y %H:%M')
    factura_id = crear_factura(cajero, items, subtotal, descuento, iva, total)
    imprimir_factura(factura_id, cajero, items, subtotal, descuento, iva, total, fecha)
    return jsonify({'ok': True, 'factura_id': factura_id})

@bp.route('/pos/productos')
@login_required
def productos():
    buscar    = request.args.get('q', '')
    categoria = request.args.get('cat', None)
    prods     = get_productos(buscar, categoria)
    return jsonify(prods)
