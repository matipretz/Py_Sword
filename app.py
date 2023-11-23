from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3, os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = "contrasenas.sqlite"
port = int(os.environ.get("PORT", 5000))


def crear_tabla():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contrasenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servicio TEXT NOT NULL,
            usuario TEXT NOT NULL,
            contrasena TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# Ruta principal
@app.route("/")
def index():
    crear_tabla()
    return render_template("index.html")


# Ruta para agregar contraseñas
@app.route("/agregar", methods=["POST"])
def agregar_contrasena():
    servicio = request.form["servicio"]
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO contrasenas (servicio, usuario, contrasena)
        VALUES (?, ?, ?)
    """,
        (servicio, usuario, contrasena),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# Ruta para ver las contraseñas
@app.route("/ver")
def ver_contrasenas():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, servicio, usuario, contrasena FROM contrasenas")
    contrasenas = cursor.fetchall()
    conn.close()

    return render_template("ver.html", contrasenas=contrasenas)


# Ruta para eliminar contraseñas
@app.route("/borrar/<int:id>", methods=["DELETE"])
def borrar_contrasena(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Obtener el nombre del servicio antes de borrar la contraseña
    cursor.execute("SELECT servicio FROM contrasenas WHERE id = ?", (id,))
    nombre_servicio = cursor.fetchone()[0]

    # Borrar la contraseña
    cursor.execute("DELETE FROM contrasenas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    # Devolver un mensaje de éxito en formato JSON con el nombre del servicio
    mensaje = {
        "mensaje": f"La contraseña para '{nombre_servicio}' fue borrada con éxito"
    }
    return jsonify(mensaje)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_contrasena(id):
    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, servicio, usuario, contrasena FROM contrasenas WHERE id = ?', (id,))
        contrasena = cursor.fetchone()
        conn.close()

        return render_template('editar.html', contrasena=contrasena)
    elif request.method == 'POST':
        nuevo_servicio = request.form['nuevo_servicio']
        nuevo_usuario = request.form['nuevo_usuario']
        nueva_contrasena = request.form['nueva_contrasena']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE contrasenas SET servicio=?, usuario=?, contrasena=? WHERE id=?',
                       (nuevo_servicio, nuevo_usuario, nueva_contrasena, id))
        conn.commit()
        conn.close()

        mensaje = {"mensaje": f"Contraseña para '{nuevo_servicio}' editada con éxito"}
        return jsonify(mensaje)


if __name__ == "__main__":
    app.run()
