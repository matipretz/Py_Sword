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
  ('Carlos Lopez', 'carlos@example.com', 'password789');

INSERT INTO contrasenas (fullname, mail, password,id_users) VALUES
  ('Juan Perez', 'juan@example.com', 'clave123','1'),
  ('Ana Rodriguez', 'ana@example.com', 'secreto456','1'),
  ('Carlos Lopez', 'carlos@example.com', 'password789','2');
