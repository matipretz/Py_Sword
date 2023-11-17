from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'contraseñas.db'

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

# Ruta para editar contraseña
@app.route('/editar', methods=['POST'])
def editar_contraseña():
    data = request.get_json()
    index = data['index']
    nueva_contrasena = data['nuevaContrasena']

    # Aquí deberías realizar la actualización en tu base de datos
    # Por ejemplo, utilizando SQLite:

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE contrasenas SET contrasena = ? WHERE id = ?', (nueva_contrasena, index))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Contraseña editada correctamente'})

# Ruta para eliminar contraseña
@app.route('/eliminar', methods=['POST'])
def eliminar_contraseña():
    data = request.get_json()
    index = data['index']

    # Aquí deberías realizar la eliminación en tu base de datos
    # Por ejemplo, utilizando SQLite:

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contrasenas WHERE id = ?', (index,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Contraseña eliminada correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
