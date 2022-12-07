-- MariaDB dump 10.19  Distrib 10.5.15-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: testing_api
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('d1c6270ca171');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_log_headers`
--

DROP TABLE IF EXISTS `audit_log_headers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_log_headers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action` varchar(50) NOT NULL,
  `table_name` varchar(50) NOT NULL,
  `record_pk` varchar(100) DEFAULT NULL,
  `user` varchar(100) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_audit_log_headers_users_badge_user` (`user`),
  KEY `ix_audit_log_headers_action` (`action`),
  KEY `ix_audit_log_headers_id` (`id`),
  KEY `ix_audit_log_headers_record_pk` (`record_pk`),
  KEY `ix_audit_log_headers_table_name` (`table_name`),
  CONSTRAINT `fk_audit_log_headers_users_badge_user` FOREIGN KEY (`user`) REFERENCES `users` (`badge`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log_headers`
--

LOCK TABLES `audit_log_headers` WRITE;
/*!40000 ALTER TABLE `audit_log_headers` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_log_headers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` varchar(100) NOT NULL,
  `project` varchar(50) NOT NULL,
  `process` varchar(50) DEFAULT NULL,
  `line` int DEFAULT NULL,
  `device_name` varchar(20) NOT NULL,
  `device_cname` varchar(100) DEFAULT NULL,
  `x_axis` float NOT NULL,
  `y_axis` float NOT NULL,
  `is_rescue` tinyint(1) DEFAULT NULL,
  `workshop` int DEFAULT NULL,
  `sop_link` varchar(128) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_devices_factory_maps_id_workshop` (`workshop`),
  KEY `ix_devices_id` (`id`),
  CONSTRAINT `fk_devices_factory_maps_id_workshop` FOREIGN KEY (`workshop`) REFERENCES `factory_maps` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factory_maps`
--

DROP TABLE IF EXISTS `factory_maps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `factory_maps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `map` json NOT NULL,
  `related_devices` json NOT NULL,
  `image` mediumblob,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_factory_maps_name` (`name`),
  KEY `ix_factory_maps_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factory_maps`
--

LOCK TABLES `factory_maps` WRITE;
/*!40000 ALTER TABLE `factory_maps` DISABLE KEYS */;
/*!40000 ALTER TABLE `factory_maps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mission_events`
--

DROP TABLE IF EXISTS `mission_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mission_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mission` int DEFAULT NULL,
  `event_id` int NOT NULL,
  `category` int NOT NULL,
  `message` varchar(100) DEFAULT NULL,
  `host` varchar(50) NOT NULL,
  `table_name` varchar(50) NOT NULL,
  `event_beg_date` datetime DEFAULT NULL,
  `event_end_date` datetime DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uc_mission_events_event_id_table_name_mission` (`event_id`,`table_name`,`mission`),
  KEY `fk_mission_events_missions_id_mission` (`mission`),
  CONSTRAINT `fk_mission_events_missions_id_mission` FOREIGN KEY (`mission`) REFERENCES `missions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission_events`
--

LOCK TABLES `mission_events` WRITE;
/*!40000 ALTER TABLE `mission_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `mission_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `missions`
--

DROP TABLE IF EXISTS `missions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `missions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `device` varchar(100) DEFAULT NULL,
  `worker` varchar(100) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `is_done` tinyint(1) DEFAULT NULL,
  `is_done_cure` tinyint(1) DEFAULT NULL,
  `is_done_shift` tinyint(1) DEFAULT NULL,
  `is_done_cancel` tinyint(1) DEFAULT NULL,
  `is_done_finish` tinyint(1) DEFAULT NULL,
  `is_lonely` tinyint(1) DEFAULT NULL,
  `is_emergency` tinyint(1) DEFAULT NULL,
  `overtime_level` int DEFAULT NULL,
  `notify_send_date` datetime DEFAULT NULL,
  `notify_recv_date` datetime DEFAULT NULL,
  `accept_recv_date` datetime DEFAULT NULL,
  `repair_beg_date` datetime DEFAULT NULL,
  `repair_end_date` datetime DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_missions_devices_id_device` (`device`),
  KEY `fk_missions_users_badge_worker` (`worker`),
  KEY `ix_missions_id` (`id`),
  CONSTRAINT `fk_missions_devices_id_device` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_missions_users_badge_worker` FOREIGN KEY (`worker`) REFERENCES `users` (`badge`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `missions`
--

LOCK TABLES `missions` WRITE;
/*!40000 ALTER TABLE `missions` DISABLE KEYS */;
/*!40000 ALTER TABLE `missions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `missions_users`
--

DROP TABLE IF EXISTS `missions_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `missions_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(100) DEFAULT NULL,
  `mission` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_missions_users_missions_mission_id` (`mission`),
  KEY `fk_missions_users_users_user_badge` (`user`),
  CONSTRAINT `fk_missions_users_missions_mission_id` FOREIGN KEY (`mission`) REFERENCES `missions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_missions_users_users_user_badge` FOREIGN KEY (`user`) REFERENCES `users` (`badge`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `missions_users`
--

LOCK TABLES `missions_users` WRITE;
/*!40000 ALTER TABLE `missions_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `missions_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shifts`
--

DROP TABLE IF EXISTS `shifts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shifts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift_beg_time` time NOT NULL,
  `shift_end_time` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_shifts_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shifts`
--

LOCK TABLES `shifts` WRITE;
/*!40000 ALTER TABLE `shifts` DISABLE KEYS */;
INSERT INTO `shifts` VALUES (1,'07:40:00','19:40:00'),(2,'19:40:00','07:40:00');
/*!40000 ALTER TABLE `shifts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_device_levels`
--

DROP TABLE IF EXISTS `user_device_levels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_device_levels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(100) DEFAULT NULL,
  `device` varchar(100) DEFAULT NULL,
  `level` smallint DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uc_user_device_levels_device_user` (`device`,`user`),
  KEY `fk_user_device_levels_users_badge_user` (`user`),
  KEY `ix_user_device_levels_id` (`id`),
  CONSTRAINT `fk_user_device_levels_devices_id_device` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_device_levels_users_badge_user` FOREIGN KEY (`user`) REFERENCES `users` (`badge`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_device_levels`
--

LOCK TABLES `user_device_levels` WRITE;
/*!40000 ALTER TABLE `user_device_levels` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_device_levels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `badge` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(100) DEFAULT NULL,
  `workshop` int DEFAULT NULL,
  `superior` varchar(100) DEFAULT NULL,
  `level` smallint NOT NULL,
  `shift` int DEFAULT NULL,
  `change_pwd` tinyint(1) DEFAULT '0',
  `current_UUID` varchar(100) DEFAULT NULL,
  `start_position` varchar(100) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `at_device` varchar(100) DEFAULT NULL,
  `shift_start_count` int DEFAULT NULL,
  `shift_reject_count` int DEFAULT NULL,
  `check_alive_time` datetime DEFAULT NULL,
  `shift_beg_date` datetime DEFAULT NULL,
  `finish_event_date` datetime DEFAULT NULL,
  `login_date` datetime DEFAULT NULL,
  `logout_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`badge`),
  KEY `fk_users_devices_id_at_device` (`at_device`),
  KEY `fk_users_shifts_id_shift` (`shift`),
  KEY `fk_users_devices_id_start_position` (`start_position`),
  KEY `fk_users_users_badge_superior` (`superior`),
  KEY `fk_users_factory_maps_id_workshop` (`workshop`),
  KEY `ix_users_badge` (`badge`),
  CONSTRAINT `fk_users_devices_id_at_device` FOREIGN KEY (`at_device`) REFERENCES `devices` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_users_devices_id_start_position` FOREIGN KEY (`start_position`) REFERENCES `devices` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_users_factory_maps_id_workshop` FOREIGN KEY (`workshop`) REFERENCES `factory_maps` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_users_shifts_id_shift` FOREIGN KEY (`shift`) REFERENCES `shifts` (`id`),
  CONSTRAINT `fk_users_users_badge_superior` FOREIGN KEY (`superior`) REFERENCES `users` (`badge`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin','admin','$5$rounds=10000$F0XL1NKPWDHaSH$x7OJPMIuQs3XFigY6rsIzhYVDezZa0i3O1qZrDemcm5',NULL,NULL,5,NULL,0,'0',NULL,NULL,NULL,0,0,'2022-12-06 14:08:54','1990-01-01 00:00:00','1990-01-01 00:00:00','1990-01-01 00:00:00','1990-01-01 00:00:00','2022-12-06 14:08:54','2022-12-06 14:08:54');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `whitelist_devices`
--

DROP TABLE IF EXISTS `whitelist_devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `whitelist_devices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device` varchar(100) NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device` (`device`),
  CONSTRAINT `fk_whitelist_devices_devices_id_device` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `whitelist_devices`
--

LOCK TABLES `whitelist_devices` WRITE;
/*!40000 ALTER TABLE `whitelist_devices` DISABLE KEYS */;
/*!40000 ALTER TABLE `whitelist_devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `whitelistdevices_users`
--

DROP TABLE IF EXISTS `whitelistdevices_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `whitelistdevices_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(100) DEFAULT NULL,
  `whitelistdevice` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_whitelistdevices_users_users_user_badge` (`user`),
  KEY `fk_whitelistdevices_users_whitelist_devices_whitelistdevice_id` (`whitelistdevice`),
  CONSTRAINT `fk_whitelistdevices_users_users_user_badge` FOREIGN KEY (`user`) REFERENCES `users` (`badge`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_whitelistdevices_users_whitelist_devices_whitelistdevice_id` FOREIGN KEY (`whitelistdevice`) REFERENCES `whitelist_devices` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `whitelistdevices_users`
--

LOCK TABLES `whitelistdevices_users` WRITE;
/*!40000 ALTER TABLE `whitelistdevices_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `whitelistdevices_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-07 16:29:30
