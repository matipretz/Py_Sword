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




--.TEST DATA

INSERT INTO usuarios (fullname, mail, password) VALUES
  ('Juan Perez', 'juan@example.com', 'clave123'),
  ('Ana Rodriguez', 'ana@example.com', 'secreto456'),
  ('TEST_USER', 'test@test.com', 'test');

INSERT INTO contrasenas (servicio, usuario, contrasena,id_users) VALUES
  ('Spotify', 'juan@example.com', 'clave123','16'),
  ('YouTube', 'ana@example.com', 'secreto456','16'),
  ('Netflix', 'carlos@example.com', 'password789','16');


--. QUERY

sql = "INSERT INTO usuarios (fullname, mail, password) VALUES (%s, %s, %s);"
data = (name, email, password)

conn = mysql.connect
cursor = conn.cursor()

try:
    cursor.execute(sql, data)
    conn.commit()