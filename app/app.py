from flask import Flask
from flask import render_template, request, redirect, jsonify, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pysword$pysword_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# LANDING
@app.route("/")
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


@app.route("/crear-registro", methods=["POST"])
def crear_registro():
    name = request.form["txtFullname"]
    email = request.form["txtEmail"]
    password = request.form["txtPassword"]

    sql = "INSERT INTO usuarios (fullname, mail, password) VALUES (%s, %s, %s);"
    data = (name, email, password)

    conn = mysql.connect
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql, data)
        conn.commit()
        return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")

    except Exception as e:
        print("Error al ejecutar la consulta SQL:", e)
        conn.rollback()
        return render_template("index.html", mensaje2="Error al registrar el usuario")



if __name__ == "__main__":
    app.secret_key = "password1234"
    app.run(debug=True)
