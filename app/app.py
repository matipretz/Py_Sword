from flask import Flask
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
    jsonify,
)
from flask_mysqldb import MySQL


app = Flask(
    __name__,
)
app.secret_key = "password1234"


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pysword$pysword_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route("/")
def inicio():
    return render_template("py_sword.html")


@app.route("/index")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    return render_template("index.html", user=data)


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/acceso-login", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
        and "txtEmail" in request.form
        and "txtPassword" in request.form
    ):
        _email = request.form["txtEmail"]
        _password = request.form["txtPassword"]

    conn = mysql.connect
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM usuarios WHERE mail = %s AND password = %s",
        (
            _email,  # type:ignore
            _password,  # type:ignore
        ),
    )
    account = cur.fetchone()
    if account:
        session["logueado"] = True
        session["fullname"] = account["fullname"]
        session["user_id"] = account["id"]
        session["id_rol"] = account["id_rol"]

        if session["id_rol"] == 1:
            return render_template("admin.html")
        elif session["id_rol"] == 2:
            return redirect("ver")
    else:
        return render_template("index.html", mensaje="Usuario o Contraseña Incorrecta")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("py_sword"))


@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/crear-registro", methods=["GET", "POST"])
def crear_registro():
    name = request.form["txtFullname"]
    email = request.form["txtEmail"]
    password = request.form["txtPassword"]

    conn = mysql.connect
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios(fullname, mail, password, id_rol) VALUES (%s, %s, %s,'2')",
        (name, email, password),
    )
    conn.commit()

    return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")


# Obtener datos de usuario para editarlos
@app.route("/edit-user/<int:id>", methods=["GET"])
def get_user(id):
    cur = mysql.connect.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    data = cur.fetchone()
    return redirect(url_for("edit-user<int:id>", user=data))


# Editar Usuario
@app.route("/edit-user/<int:id>", methods=["POST"])
def update_user(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        mail = request.form["mail"]
        password = request.form["password"]
        cur = mysql.connect.cursor()
        cur.execute(
            """
        UPDATE usuarios 
        SET fullname= %s, 
            mail = %s, 
            password = %s,
            id_rol = '2'
        WHERE id = %s           
        """,
            (fullname, mail, password, id),
        )
        mysql.connect.commit()
        return redirect(url_for("home"))


# ----------------------------------------------------------------------------


@app.route("/py_sword")
def py_sword():
    return render_template("py_sword.html")


@app.route("/ver-page")
def ver_page():
    return render_template("home.html")


@app.route("/ver", methods=["GET", "POST"])  # type:ignore
def ver():
    if "logueado" in session and session["logueado"]:
        user_id = session.get("user_id")
        if user_id is not None:
            sql = "SELECT * FROM contrasenas WHERE id_users = %s;"
            data = (user_id,)
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(sql, data)
            contrasenas = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template("home.html", contrasenas=contrasenas, user=data)


@app.route("/create-page")
def create_page():
    return render_template("crear.html")


@app.route("/agregar", methods=["POST"])  # type:ignore
def create_entradas():
    if "logueado" in session and session["logueado"]:
        user_id = session.get("user_id")
        if user_id is not None:
            servicio = request.form.get("servicio")
            usuario = request.form.get("usuario")
            contrasena = request.form.get("contrasena")

            query = "INSERT INTO contrasenas (servicio, usuario, contrasena, id_users) VALUES (%s, %s, %s, %s)"
            values = (servicio, usuario, contrasena, user_id)
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return redirect(url_for("ver"))


@app.route("/ver/<int:id>", methods=["GET"])
def get_entrada(id):
    if "logueado" in session and session["logueado"]:
        user_id = session.get("user_id")
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM contrasenas WHERE id = %s AND id_users = %s",
                (id, user_id),
            )
            entrada = cursor.fetchone()
            cursor.close()

            if entrada:
                return entrada
            else:
                abort(404)  # Página no encontrada
        except Exception as e:
            print(f"Error al obtener entrada desde la base de datos: {str(e)}")
            abort(403)  # Error interno del servidor
    else:
        return redirect(url_for("index"))


from flask import abort, redirect, url_for


@app.route("/borrar/<int:id>", methods=["DELETE"])
def delete_entrada(id):
    if "logueado" in session and session["logueado"]:
        user_id = session.get("user_id")
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            entrada = cursor.execute(
                "DELETE FROM contrasenas WHERE id = %s AND id_users = %s", (id, user_id)
            )
            conn.commit()
            cursor.close()
            if entrada:
                return entrada
            else:
                abort(404)  # Página no encontrada
        except Exception as e:
            print(f"Error al borrar entrada desde la base de datos: {str(e)}")
            abort(500)  # Error interno del servidor
    else:
        abort(403)  # Prohibido: el usuario no está logueado


@app.route("/editar/<int:id>", methods=["GET"])
def obtener_contrasena(id):
    if "logueado" in session and session["logueado"]:
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, servicio, usuario, contrasena FROM contrasenas WHERE id = %s",
                (id,),
            )

            contrasena = cursor.fetchone()
            cursor.close()
            return render_template("update.html", contrasena=contrasena)
        except Exception as e:
            print(f"Error al obtener los datos: {str(e)}")
            abort(500)


@app.route("/editar/<int:id>", methods=["POST"])
def editar_contrasena(id):
    if "logueado" in session and session["logueado"]:
        try:
            nuevo_servicio = request.form["nuevo_servicio"]
            nuevo_usuario = request.form["nuevo_usuario"]
            nueva_contrasena = request.form["nueva_contrasena"]
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE contrasenas SET servicio=%s, usuario=%s, contrasena=%s WHERE id=%s",
                (nuevo_servicio, nuevo_usuario, nueva_contrasena, id),
            )
            mysql.connect.commit()
            mysql.connect.close()
        except Exception as e:
            print(f"Error al obtener los datos: {str(e)}")
            abort(500)
        mensaje = {"mensaje": f"Contraseña para '{nuevo_servicio}' editada con éxito"}
        return jsonify(mensaje)
    else:
        abort(403)  # Prohibido: el usuario no está logueado


if __name__ == "__main__":
    app.run(debug=True)
