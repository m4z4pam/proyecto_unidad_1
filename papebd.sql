-- MySQL dump 10.13  Distrib 9.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: papebd
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'hola','3328869483','israelgutierrez038@gmail.com');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `categoria` enum('Escolares','Oficina','Arte') NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `activo` tinyint(1) DEFAULT '1',
  `costo` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Cuaderno Profesional','Escolares',45.50,111,1,27.30),(2,'Lápiz HB #4','Escolares',9.50,241,0,0.00),(3,'Bolígrafo Azul','Escolares',8.50,242,1,5.10),(4,'Mochila Escolar','Escolares',320.00,30,1,192.00),(5,'Caja de Colores 24 pzas','Escolares',95.00,52,1,57.00),(6,'Borrador Blanco','Escolares',6.50,190,1,3.90),(7,'Sacapuntas Metálico','Escolares',12.00,150,1,7.20),(8,'Juego de Geometría','Escolares',35.00,80,1,21.00),(9,'Tijeras Escolares','Escolares',25.00,90,1,15.00),(10,'Silla Ergonómica','Oficina',1850.00,2,1,1295.00),(11,'Escritorio Ejecutivo','Oficina',3250.00,8,1,2275.00),(12,'Papel Bond Carta 500 hojas','Oficina',145.00,100,1,101.50),(13,'Engrapadora Metálica','Oficina',120.00,60,1,84.00),(14,'Cinta Adhesiva Transparente','Oficina',18.00,200,1,12.60),(15,'Marcadores Permanentes 4 pzas','Oficina',75.00,80,1,52.50),(16,'Carpeta de Archivo','Oficina',25.00,180,1,17.50),(17,'Post-it Amarillo','Oficina',35.00,150,1,24.50),(18,'Organizador de Escritorio','Oficina',220.00,30,1,154.00),(19,'Pinceles de Madera 5 pzas','Arte',120.00,50,1,60.00),(20,'Lienzo Mediano 40x50cm','Arte',180.00,40,1,90.00),(21,'Acuarelas Profesionales','Arte',350.00,25,1,175.00),(22,'Óleo 12 colores','Arte',420.00,20,1,210.00),(23,'Caballeta de Madera','Arte',890.00,3,1,445.00),(24,'Arcilla para Escultura 2kg','Arte',260.00,2,1,130.00),(25,'Set de Plumones Artísticos','Arte',310.00,25,1,155.00),(26,'Lapiz HB #4','Escolares',9.50,309,1,5.70),(27,'cuerdas para guitarra estrella','Arte',520.00,0,1,260.00),(28,'lapiz prueba','Escolares',12.50,456,1,7.50),(29,'lapiz prueba','Escolares',12.50,456,0,8.50);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_proveedores`
--

DROP TABLE IF EXISTS `productos_proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_proveedores` (
  `id_relacion` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `id_proveedor` int NOT NULL,
  PRIMARY KEY (`id_relacion`),
  UNIQUE KEY `id_producto` (`id_producto`,`id_proveedor`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `productos_proveedores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE,
  CONSTRAINT `productos_proveedores_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_proveedores`
--

LOCK TABLES `productos_proveedores` WRITE;
/*!40000 ALTER TABLE `productos_proveedores` DISABLE KEYS */;
INSERT INTO `productos_proveedores` VALUES (2,1,2),(3,3,2);
/*!40000 ALTER TABLE `productos_proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `creado_en` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_proveedor`),
  UNIQUE KEY `rfc` (`rfc`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (2,'123','ABC123456DEF','9876543210','dsdasdasdsa@gmail.com','dsadasdawew3reafreafe3rf2','2025-09-15 20:55:39');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `rol` enum('admin','usuario','supervisor') DEFAULT 'usuario',
  `activo` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ultimo_login` timestamp NULL DEFAULT NULL,
  `intentos_fallidos` int DEFAULT '0',
  `bloqueado_hasta` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (7,'gerente','gf@empresa.com','$2b$12$/YZK0ibXLGi.ShkXYb/8v.fDgOPWLLxyp29xOWChjkSFexD7hELGO','a','webo','supervisor',1,'2025-09-16 05:35:42','2025-09-16 05:36:01',0,NULL),(8,'israel','israelgutierrez038@gmail.com','$2b$12$1UEz627bc9rp4rnNMla4W.e3NpaMV0I04h6bY9UqQwDib5zfkEKYi','israel','wasd','admin',1,'2025-09-16 05:38:33','2025-09-16 22:48:09',0,NULL),(10,'admin','admin@empresa.com','$2b$12$BGNRZL3Sac00voBDq3RMeONZWO6ORW3pQiqeLO6OD0gshB3lcbgj2','Administrador',NULL,'admin',1,'2025-09-16 17:20:10','2025-09-16 19:15:48',0,NULL),(11,'webo','adasdasd@gmail.com','$2b$12$hcfuwNYnd.Uo/oszS5DuuuUTAFhWeyK3tRZXvZToxDtOnYIW8pRw2','hola','sdfadfasf','usuario',1,'2025-09-16 18:40:17',NULL,0,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `id_cliente` int DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_venta`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (3,'2025-09-15 11:24:39',1,16809.00);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_detalle`
--

DROP TABLE IF EXISTS `ventas_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_detalle` (
  `id_detalle` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_venta` (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `ventas_detalle_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `ventas_detalle_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_detalle`
--

LOCK TABLES `ventas_detalle` WRITE;
/*!40000 ALTER TABLE `ventas_detalle` DISABLE KEYS */;
INSERT INTO `ventas_detalle` VALUES (24,3,16,8,25.00,200.00),(25,3,14,8,18.00,144.00),(26,3,15,10,75.00,750.00),(27,3,18,9,220.00,1980.00),(28,3,17,9,35.00,315.00),(29,3,21,13,350.00,4550.00),(30,3,23,1,890.00,890.00),(31,3,20,10,180.00,1800.00),(32,3,22,13,420.00,5460.00),(33,3,19,6,120.00,720.00);
/*!40000 ALTER TABLE `ventas_detalle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-16 17:40:46
