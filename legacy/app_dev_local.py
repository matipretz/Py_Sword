from flask import Flask
from flask import render_template, request, redirect, jsonify, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pysword$pysword_db"
mysql = MySQL(app)

# LANDING
@app.route("/")
def index():
    return render_template("index.html")


# HOME
@app.route("/home")
def home():
    cur = mysql.connect.cursor()
    cur.execute("SELECT id, servicio, usuario, contrasena FROM contrasenas")
    contrasenas = cur.fetchall()
    mysql.connect.close()
    return render_template("home.html", contrasenas=contrasenas)

# LOG-IN

@app.route("/acceso-login", methods=["GET", "POST"])
def login():
    if "txtEmail" in request.form and "txtPassword" in request.form:
        _email = request.form["txtEmail"]
        _password = request.form["txtPassword"]

        cur = mysql.connect.cursor()
        cur.execute(
            "SELECT id, fullname FROM usuarios WHERE mail = %s AND password = %s",
            (_email, _password),
        )
        user = cur.fetchone()

        if user:
            # Autenticación exitosa, almacenar el id del usuario en la sesión
            session["logueado"] = True
            session["id_usuario"] = user["id"]
            session["fullname"] = user["fullname"]
            return render_template("home.html")
        else:
            return render_template(
                "login.html", mensaje="Usuario o Contraseña Incorrectas"
            )


# CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# REGISTRO
@app.route("/registro")
def registro():
    return render_template("user_create.html")
# SING-IN
@app.route("/crear-registro", methods=["GET", "POST"])
def user_create():
    name = request.form["txtFullname"]
    email = request.form["txtEmail"]
    password = request.form["txtPassword"]

    cur = mysql.connect.cursor()
    cur.execute(
        "INSERT INTO usuarios(fullname, mail, password) VALUES (%s, %s, %s)",
        (name, email, password),
    )
    mysql.connect.commit()

    return render_template("home.html", mensaje2="Usuario Registrado Exitosamente")
    ## A FUTURO: PEDIR VALIDACION POR MAIL
    
    # ACTUALIZAR USUARIOS
@app.route("/actualizar")
def editar():
    return render_template("user_update.html")


@app.route("/actualizar-registro", methods=["GET", "POST"])
def editar_registro(id_usuario):
    if session["logueado"] == True:
        name = request.form["txtFullname"]
        email = request.form["txtEmail"]
        password = request.form["txtPassword"]

        cur = mysql.connect.cursor()
        cur.execute(
            "UPDATE usuarios SET fullname = %s, mail = %s, password = %s WHERE id_usuario = %s",
            (name, email, password, id_usuario),
        )
    mysql.connect.commit()

    return render_template("home.html", mensaje3="Usuario Modificado Exitosamente")




# Ruta para agregar contraseñas
@app.route("/agregar", methods=["GET", "POST"])
def agregar_contrasena():
    servicio = request.form["servicio"]
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]

    # Obtener el id del usuario desde la sesión
    id_usuario = session.get("id_usuario")

    if id_usuario is not None:
        cur = mysql.connect.cursor()
        cur.execute(
            """
            INSERT INTO contrasenas (servicio, usuario, contrasena, id_users)
            VALUES (%s, %s, %s, %s)
        """,
            (servicio, usuario, contrasena, id_usuario),
        )
        mysql.connect.commit()
        cur.close()

        return redirect(url_for("home"))
    else:
        # Manejar el caso donde no hay un usuario autenticado
        return "Usuario no autenticado", 403  # Código de estado HTTP 403 para acceso no autorizado






# Ruta para eliminar contraseñas
@app.route("/borrar/<int:id>", methods=["DELETE"])
def borrar_contrasena(id):
    cur = mysql.connect.cursor()

    # Obtener el nombre del servicio antes de borrar la contraseña
    cur.execute("SELECT servicio FROM contrasenas WHERE id = ?", (id,))
    nombre_servicio = cur.fetchone()[0]

    # Borrar la contraseña
    cur.execute("DELETE FROM contrasenas WHERE id = ?", (id,))
    mysql.connect.commit()
    mysql.connect.close()

    # Devolver un mensaje de éxito en formato JSON con el nombre del servicio
    mensaje = {
        "mensaje": f"La contraseña para '{nombre_servicio}' fue borrada con éxito"
    }
    return jsonify(mensaje)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_contrasena(id):
    if request.method == "GET":
        cur = mysql.connect.cursor()
        cur.execute(
            "SELECT id, servicio, usuario, contrasena FROM contrasenas WHERE id = ?",
            (id,),
        )
        contrasena = cur.fetchone()
        mysql.connect.close()

        return render_template("editar.html", contrasena=contrasena)
    elif request.method == "POST":
        nuevo_servicio = request.form["nuevo_servicio"]
        nuevo_usuario = request.form["nuevo_usuario"]
        nueva_contrasena = request.form["nueva_contrasena"]

        cur = mysql.connect.cursor()
        cur.execute(
            "UPDATE contrasenas SET servicio=?, usuario=?, contrasena=? WHERE id=?",
            (nuevo_servicio, nuevo_usuario, nueva_contrasena, id),
        )
        mysql.connect.commit()
        mysql.connect.close()

        mensaje = {"mensaje": f"Contraseña para '{nuevo_servicio}' editada con éxito"}
        return jsonify(mensaje)


if __name__ == "__main__":
    app.secret_key = "password1234"
    app.run( debug=True)
