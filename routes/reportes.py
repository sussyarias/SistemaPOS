from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from database import get_reporte_hoy, get_historial, get_factura_items
from functools import wraps

bp = Blueprint('reportes', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@bp.route('/historial')
@login_required
def historial():
    facturas = get_historial()
    return render_template('historial.html', facturas=facturas, usuario=session['usuario'])

@bp.route('/historial/detalle/<int:factura_id>')
@login_required
def detalle(factura_id):
    items = get_factura_items(factura_id)
    return jsonify({'items': items})

@bp.route('/reporte')
@login_required
def reporte():
    data = get_reporte_hoy()
    return render_template('reporte.html', data=data, usuario=session['usuario'])