-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: educhat_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class` int NOT NULL,
  `book` varchar(255) NOT NULL,
  `filepath` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (10,7,'amader_prithibi-7','books/amader_prithibi-7.txt'),(11,5,'amader-poribes-5','books/amader-poribes-5.txt'),(12,7,'blossoms-7','books/blossoms-7.txt'),(13,6,'bolsom-6','books/bolsom-6.txt'),(14,6,'Geography-6','books/Geography-6.txt'),(15,6,'history-6','books/history-6.txt'),(16,7,'history-7','books/history-7.txt'),(17,5,'patabahar-5','books/patabahar-5.txt');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_messages`
--

DROP TABLE IF EXISTS `chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `sender` enum('user','bot') NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=285 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_messages`
--

LOCK TABLES `chat_messages` WRITE;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
INSERT INTO `chat_messages` VALUES (279,37,'user','name of the book','2026-03-13 10:27:30'),(280,37,'bot','বাহবা! তুমি খুব ভালো প্রশ্ন করেছ।\n\nএই বইটির নাম হলো **\'আমাদের পরিবেশ\'**। এটি পঞ্চম শ্রেণির জন্য তৈরি করা হয়েছে, যাতে তোমরা পরিবেশ, বিজ্ঞান, সমাজ, ইতিহাস ও ভূগোল সম্পর্কে অনেক কিছু জানতে পারো।\n\nঅনেক ভালোবাসা তোমার জন্য! পড়াশোনা চালিয়ে যাও, তুমি খুব ভালো শিখবে!','2026-03-13 10:27:44'),(281,37,'user','some questions from this','2026-03-13 10:28:27'),(282,37,'bot','খুব ভালো! প্রশ্ন করা মানেই শেখার প্রথম ধাপ। তুমি তো দারুণ জিজ্ঞাসু! এই পাঠ্যবই থেকে আমি তোমার জন্য কিছু প্রশ্ন তৈরি করে দিচ্ছি, যেগুলো তোমার ভাবনাশক্তিকে আরও বাড়াতে সাহায্য করবে:\n\n১. **ত্বককে \'শরীরের বর্ম\' বলা হয়েছে কেন?** তোমার কি মনে হয়, এটি আমাদের শরীরকে কীভাবে রক্ষা করে?\n\n২. **আমাদের শরীরের কোন কোন অংশের ত্বক পাতলা এবং কোন কোন অংশের ত্বক পুরু হয়?** দুটি উদাহরণ দিয়ে বুঝিয়ে দাও। কেন এমন হয় বলে তোমার মনে হয়?\n\n৩. **মেলানিন কী এবং ত্বকের রং কালো হওয়ার সাথে এর সম্পর্ক কী?** মেলানিন কিভাবে আমাদের ত্বককে রক্ষা করে?\n\n৪. **সূর্যের আলো ত্বকের জন্য কেন উপকারী?** অতিরিক্ত রোদ লাগালে আবার কী ক্ষতি হতে পারে?\n\n৫. **ফোসকা কেন পড়ে?** পুড়ে গেলে বা ফোসকা পড়ার উপক্রম হলে সঙ্গে সঙ্গে কী করা উচিত?\n\n৬. **বয়স বাড়লে চুল সাদা হয়ে যায় কেন?**\n\nএই প্রশ্নগুলো নিয়ে তুমি একটু চিন্তা করো। দেখবে, উত্তরগুলো খুঁজে বের করতে তোমার খুব ভালো লাগবে। প্রতিটি প্রশ্নের উত্তর এই বইতেই লুকানো আছে। তুমি চেষ্টা করলেই খুঁজে পাবে!\n\nযদি কোনো প্রশ্ন বুঝতে অসুবিধা হয়, আমাকে জিজ্ঞেস করতে পারো। তোমার শেখার আগ্রহ দেখে আমি খুব খুশি! এগিয়ে যাও!','2026-03-13 10:28:45'),(283,38,'user','name of the book','2026-03-13 10:30:53'),(284,38,'bot','The name of the book is **Blossoms: English textbook for class VI**.\n\nIt\'s a wonderful book, and I\'m here to help you understand all its fascinating concepts. Keep up the great work!','2026-03-13 10:31:04');
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_sessions`
--

DROP TABLE IF EXISTS `chat_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(4) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `class_level` int NOT NULL,
  `subject` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_session_user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_sessions`
--

LOCK TABLES `chat_sessions` WRITE;
/*!40000 ALTER TABLE `chat_sessions` DISABLE KEYS */;
INSERT INTO `chat_sessions` VALUES (37,'6205','Amader Poribes 5 (Class 5)',5,'amader-poribes-5','2026-03-13 10:27:30'),(38,'6205','Bolsom 6 (Class 6)',6,'bolsom-6','2026-03-13 10:30:53');
/*!40000 ALTER TABLE `chat_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(4) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'6205','admin','scrypt:32768:8:1$QPqAyx6KfJLnVYgi$08f420ad8302b213f7b2ba529447e1322b82fe5fc37f01328d212651bceaf18f691cbaaeea2d09efdf76fa6a8d7884b35c2f53a629b7c0bfa3a69ee9d6e5d0c4','2026-03-11 20:05:24'),(2,'6867','sayantan','scrypt:32768:8:1$lGlQXLkWQzEz2Ovn$18f2774b5e6b102009a9f976981b60aedcdd8fde1cf97c3192c8a1f379b66f2cae9e32e9834f65aacbb2ceae3af97b5ae59425237cce13895ed64833db339ccf','2026-03-11 20:19:50');
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

-- Dump completed on 2026-03-13 16:08:04
