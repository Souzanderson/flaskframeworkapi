CREATE TABLE  IF NOT EXISTS `client`(
  `id` int NOT NULL AUTO_INCREMENT,
  `dsclient` varchar(450) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `email` varchar(450) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `cpfclient_UNIQUE` (`cpf`)
);

CREATE TABLE  IF NOT EXISTS `product`(
  `id` int NOT NULL AUTO_INCREMENT,
  `dsproduct` varchar(450) NOT NULL,
  `value` double NOT NULL,
  `dtupdate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
);


ALTER TABLE `client` 
ADD COLUMN `status` VARCHAR(1) NULL AFTER `email`;

ALTER TABLE `client` 
ADD COLUMN `dtupdate` datetime NULL AFTER `status`;