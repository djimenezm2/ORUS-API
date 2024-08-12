CREATE DATABASE  IF NOT EXISTS `orus_dev` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `orus_dev`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: orus_dev
-- ------------------------------------------------------
-- Server version	8.0.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ambient_moisture`
--

DROP TABLE IF EXISTS `ambient_moisture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ambient_moisture` (
  `CHIP_ID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'The ID of each client.',
  `DATA_ID` int NOT NULL COMMENT 'The ID of the data. type',
  `VALUE` float NOT NULL COMMENT 'The value measured by the chip.',
  `DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The date in which data was taken.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores relation between iot chips and ambient moisture data type.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ambient_moisture`
--

LOCK TABLES `ambient_moisture` WRITE;
/*!40000 ALTER TABLE `ambient_moisture` DISABLE KEYS */;
/*!40000 ALTER TABLE `ambient_moisture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ambient_temperature`
--

DROP TABLE IF EXISTS `ambient_temperature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ambient_temperature` (
  `CHIP_ID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'The ID of each client.',
  `DATA_ID` int NOT NULL COMMENT 'The ID of the data. type',
  `VALUE` float NOT NULL COMMENT 'The value measured by the chip.',
  `DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The date in which data was taken.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores relation between iot chips and ambient temperature data type.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ambient_temperature`
--

LOCK TABLES `ambient_temperature` WRITE;
/*!40000 ALTER TABLE `ambient_temperature` DISABLE KEYS */;
/*!40000 ALTER TABLE `ambient_temperature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_types`
--

DROP TABLE IF EXISTS `data_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_types` (
  `DATA_ID` int NOT NULL AUTO_INCREMENT COMMENT 'Incremental data id',
  `MEASURE_NAME` varchar(50) NOT NULL COMMENT 'Name of the measure taken',
  PRIMARY KEY (`DATA_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores data types which will be used in the app.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_types`
--

LOCK TABLES `data_types` WRITE;
/*!40000 ALTER TABLE `data_types` DISABLE KEYS */;
INSERT INTO `data_types` VALUES (1,'ambient_temperature'),(2,'ambient_moisture'),(3,'soil_moisture');
/*!40000 ALTER TABLE `data_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iot_chips`
--

DROP TABLE IF EXISTS `iot_chips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iot_chips` (
  `CHIP_ID` varchar(100) NOT NULL COMMENT 'The ID of each client',
  PRIMARY KEY (`CHIP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores the chip''s IDs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iot_chips`
--

LOCK TABLES `iot_chips` WRITE;
/*!40000 ALTER TABLE `iot_chips` DISABLE KEYS */;
/*!40000 ALTER TABLE `iot_chips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `soil_moisture`
--

DROP TABLE IF EXISTS `soil_moisture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `soil_moisture` (
  `CHIP_ID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'The ID of each client.',
  `DATA_ID` int NOT NULL COMMENT 'The ID of the data. type',
  `VALUE` float NOT NULL COMMENT 'The value measured by the chip.',
  `DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The date in which data was taken.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores relation between iot chips and soil temperature data type.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `soil_moisture`
--

LOCK TABLES `soil_moisture` WRITE;
/*!40000 ALTER TABLE `soil_moisture` DISABLE KEYS */;
/*!40000 ALTER TABLE `soil_moisture` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-20 20:18:10
