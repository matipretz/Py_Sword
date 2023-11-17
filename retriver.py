import os
import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('contraseñas.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contrasenas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        servicio TEXT,
        usuario TEXT,
        contrasena TEXT
    )
''')

# Ruta de la carpeta que contiene los archivos
carpeta = r'C:\Users\matip\Documents\GitHub\Py_Sword\reg'

# Leer archivos en la carpeta
for nombre_archivo in os.listdir(carpeta):
    ruta_archivo = os.path.join(carpeta, nombre_archivo)

    # Obtener el nombre del archivo sin extensión
    nombre_servicio = os.path.splitext(nombre_archivo)[0]

    # Leer el contenido del archivo
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()

    # Insertar datos en la base de datos
    cursor.execute('''
        INSERT INTO contrasenas (servicio, usuario, contrasena)
        VALUES (?, ?, ?)
    ''', (nombre_servicio, '', contenido))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Proceso completado con éxito.")
