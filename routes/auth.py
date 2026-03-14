from flask import Blueprint, render_template, request, redirect, url_for, session
from database import login as db_login

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        nombre   = request.form.get('nombre', '').strip()
        password = request.form.get('password', '').strip()
        usuario  = db_login(nombre, password)
        if usuario:
            session['usuario'] = usuario
            return redirect(url_for('pos.index'))
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render_template('login.html', error=error)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
