DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(64) NULL DEFAULT NULL,
  `email` VARCHAR(120) NULL DEFAULT NULL,
  `password_hash` VARCHAR(128) NULL DEFAULT NULL
);

DROP TABLE IF EXISTS `entrada`;
DROP TABLE IF EXISTS `entradas`;

CREATE TABLE `entrada` (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `servicio` VARCHAR(64) NULL DEFAULT NULL,
  `usuario` VARCHAR(120) NULL DEFAULT NULL,
  `contrasena` VARCHAR(128) NULL DEFAULT NULL,
  `id_users` INTEGER NULL DEFAULT NULL FOREIGN KEY (`id_users`) REFERENCES `users` (`id`)
);

-- ---
-- Test Data
-- ---

-- INSERT INTO `users` (`id`,`username`,`email`,`password_hash`) VALUES
-- ('','','','');
-- INSERT INTO `entradas` (`id`,`servicio`,`usuario`,`contrasena`,`id_users`) VALUES
-- ('','','','','');