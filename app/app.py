from flask import Flask
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


app = Flask(
    __name__,
)
app.secret_key = "password1234"


# CONEXION A LA BASE DE DATOS
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pysword$pysword_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# INICIO
@app.route("/")
def inicio():
    return render_template("py_sword.html")


# INGRESAR
@app.route("/index")
def index():
    return render_template("index.html")


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
            _email,
            _password,
        ),
    )
    account = cur.fetchone()
    # COMPROBACIÓN DEL LOGEO
    if account:
        session["logueado"] = True
        session["fullname"] = account["fullname"]
        session["user_id"] = account["id"]

        return redirect("ver")
    else:
        return render_template("index.html", mensaje="Usuario o Contraseña Incorrecta")


# CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("py_sword"))


# REGISTRO
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
        "INSERT INTO usuarios(fullname, mail, password) VALUES (%s, %s, %s)",
        (name, email, password),
    )
    conn.commit()

    return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")


# PAGINA INFORMACION
@app.route("/py_sword")
def py_sword():
    return render_template("py_sword.html")


@app.route("/ver", methods=["GET", "POST"])
def obtener_contrasenas():
    if "logueado" in session and session["logueado"]:
        user_id = session.get("user_id")
        if user_id is not None:
            sql = "SELECT * FROM contrasenas WHERE id_users = %s;"
            data = (user_id,)
            conn = mysql.connect
            cursor = conn.cursor()      
            cursor.execute(sql, data)
            contrasenas = cursor.fetchall()
            print("user_id:", user_id)
            print("contrasenas:", contrasenas)
            cursor.close()
            conn.close()
            return render_template("home.html", contrasenas=contrasenas)

                


if __name__ == "__main__":
    app.run(debug=True)
