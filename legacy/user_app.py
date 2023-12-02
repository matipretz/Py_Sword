from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__, template_folder="templates")

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "login"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# INICIO
@app.route("/")
def index():
    return render_template("index.html")


# HOME
@app.route("/home")
def admin():
    return render_template("home.html")


# LOG-IN
@app.route("/acceso-login", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
        and "txtEmail" in request.form
        and "txtPassword" in request.form
    ):
        _email = request.form["txtEmail"]
        _password = request.form["txtPassword"]

    cur = mysql.connect.cursor()
    cur.execute(
        "SELECT * FROM usuarios WHERE mail = %s AND password = %s",
        (
            _email,
            _password,
        ),
    )
    account = cur.fetchone()
    # COMPROBACIÓN DEL LOGEO
    if account:
        session["logueado"] = True
        session["fullname"] = account["fullname"]

        return render_template("home.html")
    else:
        return render_template("index.html", mensaje="Usuario O Contraseña Incorrectas")


# CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# REGISTRO
@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/crear-registro", methods=["GET", "POST"])
def crear_registro():
    name = request.form["txtFullname"]
    email = request.form["txtEmail"]
    password = request.form["txtPassword"]

    cur = mysql.connect.cursor()
    cur.execute(
        "INSERT INTO usuarios(fullname, mail, password) VALUES (%s, %s, %s)",
        (name, email, password),
    )
    mysql.connect.commit()

    return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")


# ACTUALIZAR USUARIOS
@app.route("/actualizar")
def editar():
    return render_template("actualizar.html")


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


if __name__ == "__main__":
    app.secret_key = "password1234"
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
