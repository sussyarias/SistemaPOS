from flask import Flask, redirect, url_for, session
from routes import auth, pos, inventario, reportes

app = Flask(__name__)
app.secret_key = 'pos_secret_key_2026'

app.register_blueprint(auth.bp)
app.register_blueprint(pos.bp)
app.register_blueprint(inventario.bp)
app.register_blueprint(reportes.bp)

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('pos.index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
