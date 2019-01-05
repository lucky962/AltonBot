-- MySQL dump 10.17  Distrib 10.3.11-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: AltonBot
-- ------------------------------------------------------
-- Server version	10.3.11-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `trainingsessions`
--

DROP TABLE IF EXISTS `trainingsessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trainingsessions` (
  `ID` bigint(20) NOT NULL,
  `TrainingType` text NOT NULL,
  `TrainingTime` datetime NOT NULL,
  `Host` text NOT NULL,
  `Cohost` text DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainingsessions`
--

LOCK TABLES `trainingsessions` WRITE;
/*!40000 ALTER TABLE `trainingsessions` DISABLE KEYS */;
INSERT INTO `trainingsessions` VALUES (528579138681044992,'Experienced Driver Training','2019-01-03 13:00:00','<@244596682531143680>','<@346297210847232002>'),(529932358850314240,'Dispatcher Training','2019-01-05 12:00:00','<@244596682531143680>','pm lucky9621 for requests'),(530002664210300939,'Experienced Driver Training','2019-01-04 11:00:00','<@527551160295489546>','<@244596682531143680>'),(530927609404719115,'Experienced Driver Training','2019-01-05 14:00:00','<@346297210847232002>',NULL);
/*!40000 ALTER TABLE `trainingsessions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-05 15:07:07
