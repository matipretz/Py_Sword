from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))

    def __init__(self, servicio, usuario, contrasena):
        self.servicio = servicio
        self.usuario = usuario
        self.contrasena = contrasena

with app.app_context():
    db.create_all()

# Definición del esquema para la clase Producto
class EntradaSchema(ma.Schema):
    class Meta:
        fields = ("id", "servicio", "usuario", "contrasena")

entrada_schema = EntradaSchema()  # Objeto para serializar/deserializar un producto
entradas_schema = EntradaSchema(
    many=True
)  # Objeto para serializar/deserializar múltiples productos

@app.route("/entradas", methods=["GET"])
def get_Entradas():
    all_entradas = (
        Entrada.query.all()
    )  # Obtiene todos los registros de la tabla de entradas
    result = entradas_schema.dump(
        all_entradas
    )  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/entradas/<id>", methods=["GET"])
def get_entrada(id):
    entrada = Entrada.query.get(id)  # Obtiene la entrada correspondiente al ID recibido
    return entrada_schema.jsonify(entrada)  # Retorna el JSON

@app.route("/entradas/<id>", methods=["DELETE"])
def delete_entrada(id):
    producto = Entrada.query.get(id)
    db.session.delete(producto)  # Elimina
    db.session.commit()  # Guarda los cambios en la base de datos
    return entrada_schema.jsonify(producto)  # Retorna el JSON

@app.route("/entradas", methods=["POST"])  # Endpoint para crear una entrada
def create_entradas():
    servicio = request.json["servicio"]
    usuario = request.json["usuario"]
    contrasena = request.json["contrasena"]
    new_entrada = Entrada(
        servicio, usuario, contrasena
    )  # Crea un nuevo objeto Entrada con los datos proporcionados
    db.session.add(
        new_entrada
    )  # Agrega la nueva entrada a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return entrada_schema.jsonify(
        new_entrada
    )  # Retorna el JSON de la nueva entrada creada

@app.route("/entradas/<id>", methods=["PUT"])  # Endpoint para actualizar
def update_entrada(id):
    entrada = Entrada.query.get(id)
    servicio = request.json["servicio"]
    usuario = request.json["usuario"]
    contrasena = request.json["contrasena"]
    db.session.commit()  # Guarda los cambios en la base de datos
    return entrada_schema.jsonify(entrada)  # Retorna el JSON del producto actualizado

if __name__ == "__main__":
    app.run(debug=True, port=5000)
