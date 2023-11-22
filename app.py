from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'contrasenas.db'
port = int(os.environ.get("PORT", 5000))

def crear_tabla():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contrasenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servicio TEXT NOT NULL,
            usuario TEXT NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal
@app.route('/')
def index():
    crear_tabla()
    return render_template('index.html')

# Ruta para agregar contraseñas
@app.route('/agregar', methods=['POST'])
def agregar_contrasena():
    servicio = request.form['servicio']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contrasenas (servicio, usuario, contrasena)
        VALUES (?, ?, ?)
    ''', (servicio, usuario, contrasena))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Ruta para ver las contraseñas
@app.route('/ver')
def ver_contrasenas():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT servicio, usuario, contrasena FROM contrasenas')
    contrasenas = cursor.fetchall()
    conn.close()

    return render_template('ver.html', contrasenas=contrasenas)

if __name__ == '__main__':
    app.run()
