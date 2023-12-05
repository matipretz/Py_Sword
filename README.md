<div align="center">
    <a href="https://github.com/matipretz/Py_Sword"><h1>PySword - Python Password Manager - TFO - CaC 4.0 Q2 - Com 23542</h1></a>
    <img alt="bac logo" src="readme/logo-CAC.png" height="100px" />
    <img alt="cac logo" src="readme/bac.png" height="100px" />  
</div>

## Menú
A. [Título y Descripción del Proyecto](#título-y-descripción-del-proyecto)

B. [Casos de Uso](#casos-de-uso)

B. [Instrucciones de clonado y desarrollo](#instrucciones-de-clonado-y-desarrollo)   

C. [Integrantes del Equipo](#integrantes-del-equipo)

D. [Links](#links)


## Título y Descripción del Proyecto:
- Título: "PySword - Python Password Manager"
- Descripción: PySword es un administrador de contraseñas desarrollado en Python que proporciona una solución segura y eficiente para gestionar y almacenar contraseñas de manera centralizada. Su objetivo principal es ayudar a los usuarios a mantener sus contraseñas de forma organizada y segura.


## Casos de uso:
- Gestión Segura de Contraseñas: PySword permite a los usuarios almacenar y organizar sus contraseñas de manera segura, brindando un lugar centralizado para acceder a credenciales de diversas cuentas.

- Generación de Contraseñas Fuertes: Ofrece la capacidad de generar contraseñas fuertes y aleatorias, contribuyendo así a mejorar la seguridad al crear credenciales robustas para diferentes servicios en línea.

- Eliminación de la Carga de Recordar Contraseñas: Al centralizar la gestión de contraseñas, PySword alivia la carga de recordar múltiples credenciales. Los usuarios pueden confiar en el administrador para acceder a sus contraseñas de manera segura cuando sea necesario.

## Instrucciones de clonado y desarrollo:
Puedes usar la terminal de tu sistema operativo o la terminal integrada en tu entorno de desarrollo, como VSCode.
Navega a la carpeta donde deseas clonar el repositorio utilizand el comando cd para cambiar al directorio deseado. Por ejemplo:
```bash
cd ruta/donde/quieres/clonar
```
Luego utiliza el siguiente comando para clonar el repositorio:
```bash
git clone https://github.com/matipretz/Py_Sword.git
```
Esto descargará el repositorio en tu máquina local.

Luego accede al directorio del repositorio:
```bash
cd Py_Sword
```
¡Listo!
Ahora tienes el repositorio clonado en tu máquina y estás dentro de su directorio. Puedes comenzar a trabajar en él.

---
El siguiente paso es crear un entrono de desarrollo virtual. 'venv' es un módulo que viene incluido en la biblioteca estándar de Python. La aplicacion esta desarrollada con Python 3.10.0, por lo que requiere tener instalada dicha versión. Puedes hacerlo con el siguiente comando:
```bash
py -3.10 -m venv env310
```
Esto creará una carpeta llamada venv que contendrá tu entorno virtual. Ahora activa tu entorno virtual:
En Windows, usa este comando:
```bash
.\env310\Scripts\activate
```
En sistemas Unix o MacOS:
```bash
source env310/bin/activate
```
Con el entorno virtual activado, ahora puedes instalar las dependencias desde el archivo requirements.txt:
```bash
pip install -r requirements.txt
```
Y con tu cliente SQL preferido, solo queda crear la base de datos:
```SQL
CREATE DATABASE pysword$pysword_db;

DROP TABLE IF EXISTS `contrasenas`;
DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fullname` VARCHAR(64) NULL DEFAULT NULL,
  `mail` VARCHAR(120) NULL DEFAULT NULL,
  `password` VARCHAR(128) NULL DEFAULT NULL
);


CREATE TABLE contrasenas (
  id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  servicio VARCHAR(64) NULL DEFAULT NULL,
  usuario VARCHAR(120) NULL DEFAULT NULL,
  contrasena VARCHAR(128) NULL DEFAULT NULL,
  id_users INTEGER NULL DEFAULT NULL,
  FOREIGN KEY (id_users) REFERENCES usuarios (id)
);
```
Asegúrate de que estás en la misma carpeta que tu archivo requirements.txt cuando ejecutas este comando.

Recuerda que es una buena práctica desactivar el entorno virtual cuando hayas terminado de trabajar en tu proyecto:
```bash
deactivate
```
Al ejecutar este comando, el entorno virtual se desactivará, y volverás al entorno de Python global de tu sistema.

---
Ahora, puedes ejecutar la aplicación:
```bash
python app.py
```
Este comando iniciará la aplicación en el servidor local. Puedes acceder a ella desde tu navegador visitando http://127.0.0.1:5000/


## Integrantes del Equipo:
- [Matias Martin Murad Pretz](https://www.linkedin.com/in/matiasmurad/) (representante)
- [Carolina Cuello Luna](https://www.linkedin.com/in/carolina-cuello-luna-982035233/)

## Links:
- [Contacto](mailto:mati.pretz+py_sword@googlemail.com?subject=[Py_Sword])
- [Repositorio](https://github.com/matipretz/Py_Sword)
- [App](http://pysword.pythonanywhere.com/)


### [<svg height="1rem" viewBox="0 0 512 512"><path d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM135.1 217.4c-4.5 4.2-7.1 10.1-7.1 16.3c0 12.3 10 22.3 22.3 22.3H208v96c0 17.7 14.3 32 32 32h32c17.7 0 32-14.3 32-32V256h57.7c12.3 0 22.3-10 22.3-22.3c0-6.2-2.6-12.1-7.1-16.3L269.8 117.5c-3.8-3.5-8.7-5.5-13.8-5.5s-10.1 2-13.8 5.5L135.1 217.4z" fill="grey"/></svg> Subir](#menú)