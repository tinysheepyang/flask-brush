-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: 192.168.0.75    Database: brush
-- ------------------------------------------------------
-- Server version	5.1.73-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Cases`
--

DROP TABLE IF EXISTS `Cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` varchar(100) NOT NULL,
  `url` varchar(100) NOT NULL,
  `created_time` datetime DEFAULT NULL,
  `comment` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cases`
--

LOCK TABLES `Cases` WRITE;
/*!40000 ALTER TABLE `Cases` DISABLE KEYS */;
INSERT INTO `Cases` VALUES (8,'一猫汽车网汽车电商,','http://news.emao.com/news/201511/16445.html','2016-11-17 18:52:47','0'),(9,'打通汽车电商任督二脉 一猫汽车网,','http://010xww.com/html/2016/10/28/53021.html','2016-11-17 18:53:05','0'),(10,'一猫汽车网选车买车,','http://news.emao.com/news/201506/9824.html','2016-11-17 18:53:21','0'),(11,'一猫汽车网购车优惠,','http://mall.emao.com/city/beijing/','2016-11-17 18:53:41','0'),(12,'一猫汽车网底价买车','http://news.emao.com/news/201501/4483.html','2016-11-17 18:53:57','0'),(13,'一猫汽车网 汽车电商,','http://news.emao.com/news/201511/16445.html','2016-11-17 18:54:16','0'),(14,'一猫汽车网 选车买车,','http://news.emao.com/news/201506/9824.html','2016-11-17 18:54:31','0'),(15,'一猫汽车网 购车优惠,','http://mall.emao.com/city/beijing/','2016-11-17 18:54:47','0'),(16,'一猫汽车网 底价买车,','http://news.emao.com/news/201501/4483.html','2016-11-17 18:55:19','0'),(17,'双十一活动 一猫汽车网,','http://news.emao.com/news/201511/15283.html','2016-11-17 18:56:14','0'),(18,'双11汽车电商大战升温 一猫百辆名车','http://www.020xww.com/html/2016/11/07/11255.html','2016-11-17 18:56:36','0'),(19,'一猫双11轻松“贷”,','http://car.southcn.com/7/2016-11/11/content_159533175.htm','2016-11-17 18:56:54','0'),(20,'双十一电商再开战 猫狗撩人各有大招','http://www.hubsc.com/cfy/20161116103007.html','2016-11-17 18:57:12','0'),(21,'一猫汽车网','random.choice(env.NEWS)','2016-11-17 19:06:24','0'),(22,'一猫汽车网','random.choice(env.HOMEPAGE)','2016-11-17 19:06:43','0'),(23,'一猫汽车网','random.choice(env.AUTO)','2016-11-17 19:07:00','0'),(24,'一猫汽车网','random.choice(env.DEALER)','2016-11-17 19:07:19','0'),(25,'一猫汽车网','random.choice(env.MALL)','2016-11-17 19:07:47','0'),(26,'一猫汽车网','http://ask.emao.com','2016-11-17 19:08:11','0'),(27,'一猫汽车网','random.choice(env.CITY)','2016-11-17 19:08:34','0'),(28,'汽车电商“约惠“广州车展 一猫汽车网福利来袭','http://beijing.auto.ifeng.com/shangqing/2016/1117/36274.shtml','2016-11-18 11:57:56','0');
/*!40000 ALTER TABLE `Cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` varchar(40) NOT NULL,
  `registered_on` datetime NOT NULL,
  `admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'chenshiyang460@emao.com','123qwe','2016-11-04 11:39:13',0),(2,'zhangxuejun074@emao.com','123456','2016-11-18 17:45:26',0),(3,'zhoubangjun538@emao.com','123456','2017-03-10 17:06:18',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-12 17:37:09
