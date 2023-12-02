from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

CORS(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:@localhost/pysword$pysword_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(64))
    usuario = db.Column(db.String(120))
    contrasena = db.Column(db.String(128))
    id_users = db.Column(db.String(128))

    def __init__(self, servicio, usuario, contrasena, id_users):
        self.servicio = servicio
        self.usuario = usuario
        self.contrasena = contrasena
        self.id_users = id_users


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash


with app.app_context():
    db.create_all()


# Definición del esquema para la clase Entrada
class EntradaSchema(ma.Schema):
    class Meta:
        fields = ("id", "servicio", "usuario", "contrasena", "id_users")


entrada_schema = EntradaSchema()  # Objeto para serializar/deserializar una entrada
entradas_schema = EntradaSchema(
    many=True
)  # Objeto para serializar/deserializar múltiples entradas


# Definición del esquema para la clase User
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "password_hash")


usuario_schema = UsuarioSchema()  # Objeto para serializar/deserializar un usuario
usuarios_schema = UsuarioSchema(
    many=True
)  # Objeto para serializar/deserializar múltiples usuarios


@app.route("/ver", methods=["GET"])
def get_Entradas():
    all_entradas = (
        Entrada.query.all()
    )  # Obtiene todos los registros de la tabla de entradas
    result = entradas_schema.dump(
        all_entradas
    )  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla


@app.route("/ver/<id>", methods=["GET"])
def get_entrada(id):
    entrada = Entrada.query.get(id)  # Obtiene la entrada correspondiente al ID recibido
    return entrada_schema.jsonify(entrada)  # Retorna el JSON


@app.route("/ver/<id>", methods=["DELETE"])
def delete_entrada(id):
    entrada = Entrada.query.get(id)
    db.session.delete(entrada)  # Elimina
    db.session.commit()  # Guarda los cambios en la base de datos
    return entrada_schema.jsonify(entrada)  # Retorna el JSON


@app.route("/create", methods=["POST"])  # Endpoint para crear una entrada
def create_entradas():
    servicio = request.json["servicio"]
    usuario = request.json["usuario"]
    contrasena = request.json["contrasena"]
    id_users = usuario.query.get(id)
    new_entrada = Entrada(
        servicio, usuario, contrasena, id_users
    )  # Crea un nuevo objeto Entrada con los datos proporcionados
    db.session.add(
        new_entrada
    )  # Agrega la nueva entrada a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return entrada_schema.jsonify(
        new_entrada
    )  # Retorna el JSON de la nueva entrada creada


@app.route("/ver/<id>", methods=["PUT"])  # Endpoint para actualizar
def update_entrada(id):
    entrada = Entrada.query.get(id)
    servicio = request.json["servicio"]
    usuario = request.json["usuario"]
    contrasena = request.json["contrasena"]
    db.session.commit()  # Guarda los cambios en la base de datos
    return entrada_schema.jsonify(entrada)  # Retorna el JSON de la entrada actualizado


if __name__ == "__main__":
    app.run(debug=True, port=5000)
