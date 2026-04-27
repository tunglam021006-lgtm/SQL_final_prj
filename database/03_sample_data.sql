-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: personal_finance_db
-- ------------------------------------------------------
-- Server version	8.4.7

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
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add account',9,'add_account'),(34,'Can change account',9,'change_account'),(35,'Can delete account',9,'delete_account'),(36,'Can view account',9,'view_account'),(37,'Can add budget',10,'add_budget'),(38,'Can change budget',10,'change_budget'),(39,'Can delete budget',10,'delete_budget'),(40,'Can view budget',10,'view_budget'),(41,'Can add category',11,'add_category'),(42,'Can change category',11,'change_category'),(43,'Can delete category',11,'delete_category'),(44,'Can view category',11,'view_category'),(45,'Can add transaction',12,'add_transaction'),(46,'Can change transaction',12,'change_transaction'),(47,'Can delete transaction',12,'delete_transaction'),(48,'Can view transaction',12,'view_transaction'),(49,'Can add financial goal',13,'add_financialgoal'),(50,'Can change financial goal',13,'change_financialgoal'),(51,'Can delete financial goal',13,'delete_financialgoal'),(52,'Can view financial goal',13,'view_financialgoal'),(53,'Can add recurring transaction',14,'add_recurringtransaction'),(54,'Can change recurring transaction',14,'change_recurringtransaction'),(55,'Can delete recurring transaction',14,'delete_recurringtransaction'),(56,'Can view recurring transaction',14,'view_recurringtransaction');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(9,'finance','account'),(10,'finance','budget'),(11,'finance','category'),(13,'finance','financialgoal'),(14,'finance','recurringtransaction'),(12,'finance','transaction'),(5,'sessions','session'),(8,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-04-23 07:03:55.716857'),(2,'contenttypes','0002_remove_content_type_name','2026-04-23 07:03:55.775714'),(3,'auth','0001_initial','2026-04-23 07:03:55.935766'),(4,'auth','0002_alter_permission_name_max_length','2026-04-23 07:03:55.980922'),(5,'auth','0003_alter_user_email_max_length','2026-04-23 07:03:55.987398'),(6,'auth','0004_alter_user_username_opts','2026-04-23 07:03:56.000846'),(7,'auth','0005_alter_user_last_login_null','2026-04-23 07:03:56.006846'),(8,'auth','0006_require_contenttypes_0002','2026-04-23 07:03:56.009846'),(9,'auth','0007_alter_validators_add_error_messages','2026-04-23 07:03:56.015850'),(10,'auth','0008_alter_user_username_max_length','2026-04-23 07:03:56.021851'),(11,'auth','0009_alter_user_last_name_max_length','2026-04-23 07:03:56.028847'),(12,'auth','0010_alter_group_name_max_length','2026-04-23 07:03:56.045985'),(13,'auth','0011_update_proxy_permissions','2026-04-23 07:03:56.053012'),(14,'auth','0012_alter_user_first_name_max_length','2026-04-23 07:03:56.059625'),(15,'users','0001_initial','2026-04-23 07:03:56.257295'),(16,'admin','0001_initial','2026-04-23 07:03:56.323738'),(17,'admin','0002_logentry_remove_auto_add','2026-04-23 07:03:56.330720'),(18,'admin','0003_logentry_add_action_flag_choices','2026-04-23 07:03:56.337582'),(19,'authtoken','0001_initial','2026-04-23 07:03:56.380532'),(20,'authtoken','0002_auto_20160226_1747','2026-04-23 07:03:56.397654'),(21,'authtoken','0003_tokenproxy','2026-04-23 07:03:56.402658'),(22,'authtoken','0004_alter_tokenproxy_options','2026-04-23 07:03:56.409347'),(23,'finance','0001_initial','2026-04-23 07:03:56.465344'),(24,'finance','0002_initial','2026-04-23 07:03:56.761428'),(25,'finance','0003_alter_budget_category_alter_transaction_category','2026-04-23 07:03:56.774125'),(26,'sessions','0001_initial','2026-04-23 07:03:56.800065'),(27,'finance','0004_account_balance_account_bank_name_and_more','2026-04-23 08:06:20.572198'),(28,'finance','0005_financialgoal_recurringtransaction_and_more','2026-04-24 12:52:39.159314');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2rhv9u23x3gaweaq8cyswtgi9kede6jt','.eJxVjU0OgjAQhe_StWmmQ7WMS_ecgUyno6CkJBRWxrtbEhaavNX7-d7b9LytQ78VXfoxmatBc_r1IstL8x6kJ-fHbGXO6zJGu1fskRbbzUmn29H9Awxchrrm0KTggwIRIpCiaxIyi4ADDIAtatR7uLgGPJGXFqjqTK4NXoi4Qqf6X0mazecLV4s5vw:1wGI2d:RFyWdFirG2C86M0xodJF7eLJFUZsuqBOn7XJVnwMClk','2026-05-08 15:02:03.637587');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `finance_account`
--

LOCK TABLES `finance_account` WRITE;
/*!40000 ALTER TABLE `finance_account` DISABLE KEYS */;
INSERT INTO `finance_account` VALUES (1,1,'Tiền ăn','cash','VND',100000,'2026-04-23 10:59:55.894514',1,100000,NULL),(2,1,'Tài khoản lương','bank','VND',1500000,'2026-04-23 11:16:07.672247',1,1550000,'MBBank'),(3,1,'Cash Wallet','cash','VND',3000000,'2026-04-23 13:21:42.886353',2,6100000,NULL),(4,1,'MB Bank','bank','VND',15000000,'2026-04-23 13:21:42.892350',2,117130000,'MB Bank'),(5,1,'Momo','e-wallet','VND',1000000,'2026-04-23 13:21:42.894359',2,4120000,'Momo');
/*!40000 ALTER TABLE `finance_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `finance_budget`
--

LOCK TABLES `finance_budget` WRITE;
/*!40000 ALTER TABLE `finance_budget` DISABLE KEYS */;
INSERT INTO `finance_budget` VALUES (1,3000000,'monthly','2026-04-23 13:21:42.915382',2,7,80.00,4,2026),(2,1200000,'monthly','2026-04-23 13:21:42.921353',2,8,80.00,4,2026),(3,2000000,'monthly','2026-04-23 13:21:42.924376',2,9,80.00,4,2026),(4,1000000,'monthly','2026-04-23 13:21:42.928353',2,10,80.00,4,2026);
/*!40000 ALTER TABLE `finance_budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `finance_category`
--

LOCK TABLES `finance_category` WRITE;
/*!40000 ALTER TABLE `finance_category` DISABLE KEYS */;
INSERT INTO `finance_category` VALUES (1,1,'Lương','income',NULL,1),(2,1,'Làm chính','income',1,1),(3,1,'Làm thêm','income',1,1),(4,1,'Salary','income',NULL,2),(5,1,'Bonus','income',NULL,2),(6,1,'Freelance','income',NULL,2),(7,1,'Food','expense',NULL,2),(8,1,'Transport','expense',NULL,2),(9,1,'Shopping','expense',NULL,2),(10,1,'Bills','expense',NULL,2),(11,1,'Entertainment','expense',NULL,2),(12,1,'Breakfast','expense',7,2),(13,1,'Coffee','expense',7,2);
/*!40000 ALTER TABLE `finance_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `finance_financialgoal`
--

LOCK TABLES `finance_financialgoal` WRITE;
/*!40000 ALTER TABLE `finance_financialgoal` DISABLE KEYS */;
INSERT INTO `finance_financialgoal` VALUES (1,'Mua Macbook',30000000.00,500000.00,'2026-10-30','',1,'2026-04-24 13:07:20.876949','2026-04-24 13:07:20.876949',2);
/*!40000 ALTER TABLE `finance_financialgoal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `finance_recurringtransaction`
--

LOCK TABLES `finance_recurringtransaction` WRITE;
/*!40000 ALTER TABLE `finance_recurringtransaction` DISABLE KEYS */;
INSERT INTO `finance_recurringtransaction` VALUES (1,'Lương hàng tháng','income',10000000.00,'monthly','2026-06-24',0,'2026-04-24 13:22:49.252922','',1,'2026-04-24 13:13:34.012077','2026-04-24 13:22:49.252922',4,NULL,4,2);
/*!40000 ALTER TABLE `finance_recurringtransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `finance_transaction`
--

LOCK TABLES `finance_transaction` WRITE;
/*!40000 ALTER TABLE `finance_transaction` DISABLE KEYS */;
INSERT INTO `finance_transaction` VALUES (1,'income',50000,'','2026-04-23 11:16:56.498116','2026-04-23 11:16:56.502103',2,3,NULL,1),(2,'income',25000000,'Monthly salary','2026-04-02 02:00:00.000000','2026-04-23 13:21:42.932360',4,4,NULL,2),(3,'income',3000000,'Freelance project','2026-04-06 02:00:00.000000','2026-04-23 13:21:42.936352',5,6,NULL,2),(4,'income',2000000,'Performance bonus','2026-04-13 02:00:00.000000','2026-04-23 13:21:42.939353',4,5,NULL,2),(5,'transfer',2000000,'Withdraw cash for daily spending','2026-04-03 02:00:00.000000','2026-04-23 13:21:42.944351',4,NULL,3,2),(6,'transfer',1000000,'Top up e-wallet','2026-04-09 02:00:00.000000','2026-04-23 13:21:42.947351',4,NULL,5,2),(7,'expense',250000,'Breakfasts','2026-04-04 02:00:00.000000','2026-04-23 13:21:42.951366',3,12,NULL,2),(8,'expense',180000,'Coffee with friends','2026-04-05 02:00:00.000000','2026-04-23 13:21:42.955353',5,13,NULL,2),(9,'expense',850000,'Groceries and meals','2026-04-08 02:00:00.000000','2026-04-23 13:21:42.960352',4,7,NULL,2),(10,'expense',650000,'Fuel and parking','2026-04-11 02:00:00.000000','2026-04-23 13:21:42.963352',3,8,NULL,2),(11,'expense',2400000,'New clothes and shoes','2026-04-16 02:00:00.000000','2026-04-23 13:21:42.967352',4,9,NULL,2),(12,'expense',900000,'Electricity and internet','2026-04-19 02:00:00.000000','2026-04-23 13:21:42.971352',4,10,NULL,2),(13,'expense',700000,'Movie and dinner','2026-04-21 02:00:00.000000','2026-04-23 13:21:42.985351',5,11,NULL,2),(14,'expense',450000,'Weekend family meal','2026-04-23 02:00:00.000000','2026-04-23 13:21:42.988352',4,7,NULL,2),(15,'income',22000000,'Salary 1 month(s) ago','2026-03-03 02:00:00.000000','2026-04-23 13:21:42.991352',4,4,NULL,2),(16,'expense',1200000,'Food spending 1 month(s) ago','2026-03-08 02:00:00.000000','2026-04-23 13:21:42.996372',4,7,NULL,2),(17,'expense',500000,'Transport spending 1 month(s) ago','2026-03-12 02:00:00.000000','2026-04-23 13:21:43.000889',3,8,NULL,2),(18,'expense',1300000,'Bills 1 month(s) ago','2026-03-17 02:00:00.000000','2026-04-23 13:21:43.006696',4,10,NULL,2),(19,'transfer',1000000,'Transfer 1 month(s) ago','2026-03-22 02:00:00.000000','2026-04-23 13:21:43.012198',4,NULL,3,2),(20,'income',22000000,'Salary 2 month(s) ago','2026-02-01 02:00:00.000000','2026-04-23 13:21:43.018195',4,4,NULL,2),(21,'expense',1200000,'Food spending 2 month(s) ago','2026-02-06 02:00:00.000000','2026-04-23 13:21:43.023195',4,7,NULL,2),(22,'expense',500000,'Transport spending 2 month(s) ago','2026-02-10 02:00:00.000000','2026-04-23 13:21:43.026195',3,8,NULL,2),(23,'expense',1300000,'Bills 2 month(s) ago','2026-02-15 02:00:00.000000','2026-04-23 13:21:43.030195',4,10,NULL,2),(24,'transfer',1000000,'Transfer 2 month(s) ago','2026-02-20 02:00:00.000000','2026-04-23 13:21:43.034197',4,NULL,3,2),(25,'income',22000000,'Salary 3 month(s) ago','2026-01-02 02:00:00.000000','2026-04-23 13:21:43.037309',4,4,NULL,2),(26,'expense',1200000,'Food spending 3 month(s) ago','2026-01-07 02:00:00.000000','2026-04-23 13:21:43.041402',4,7,NULL,2),(27,'expense',500000,'Transport spending 3 month(s) ago','2026-01-11 02:00:00.000000','2026-04-23 13:21:43.046132',3,8,NULL,2),(28,'expense',1300000,'Bills 3 month(s) ago','2026-01-16 02:00:00.000000','2026-04-23 13:21:43.051142',4,10,NULL,2),(29,'transfer',1000000,'Transfer 3 month(s) ago','2026-01-21 02:00:00.000000','2026-04-23 13:21:43.055037',4,NULL,3,2),(30,'income',22000000,'Salary 4 month(s) ago','2025-12-03 02:00:00.000000','2026-04-23 13:21:43.060504',4,4,NULL,2),(31,'expense',1200000,'Food spending 4 month(s) ago','2025-12-08 02:00:00.000000','2026-04-23 13:21:43.063829',4,7,NULL,2),(32,'expense',500000,'Transport spending 4 month(s) ago','2025-12-12 02:00:00.000000','2026-04-23 13:21:43.066983',3,8,NULL,2),(33,'expense',1300000,'Bills 4 month(s) ago','2025-12-17 02:00:00.000000','2026-04-23 13:21:43.069979',4,10,NULL,2),(34,'transfer',1000000,'Transfer 4 month(s) ago','2025-12-22 02:00:00.000000','2026-04-23 13:21:43.074970',4,NULL,3,2),(35,'expense',50000,'Quick Add: 50k uống cafe','2026-04-23 14:56:06.039951','2026-04-23 14:56:06.044961',4,7,NULL,2),(36,'expense',20000,'Quick Add: 20k mua áo mưa','2026-04-23 14:56:24.521406','2026-04-23 14:56:24.524412',4,7,NULL,2),(37,'expense',100000,'Quick Add: 100k mua quần áo','2026-04-23 14:56:39.342429','2026-04-23 14:56:39.345431',4,7,NULL,2),(38,'expense',50000,'Quick Add: 50k mua quần','2026-04-23 15:16:08.830174','2026-04-23 15:16:08.835149',4,7,NULL,2),(39,'expense',50000,'Quick Add: 50k mua áo','2026-04-23 15:27:13.819707','2026-04-23 15:27:13.823712',4,9,NULL,2),(40,'expense',1000000,'Quick Add: 1 triệu tiền đồ ăn','2026-04-23 17:17:35.962374','2026-04-23 17:17:35.964294',4,12,NULL,2),(41,'income',10000000,'Recurring: Lương hàng tháng','2026-04-24 13:22:49.246960','2026-04-24 13:22:49.248878',4,NULL,NULL,2);
/*!40000 ALTER TABLE `finance_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$600000$TRTXXgNHOvozFt0IyjcKBT$825YPxapxH00ZaC0IzbUV5HKpL/bNv6xNWfFFchWZc8=','2026-04-23 11:02:51.827820',1,'admin1','','','tunglam021006@gmail.com',1,1,'2026-04-23 07:05:38.153028',NULL),(2,'pbkdf2_sha256$600000$YqqOINPKMsurqhWyjCRHSg$YZ5R4p4H3xwloPG7NcoxkgjL05s86kPVSWBn3DnlQJo=','2026-04-23 13:22:55.282567',0,'taikhoantest','','','demo@expense.local',0,1,'2026-04-23 13:21:42.673354','Demo User');
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-24 22:13:35
