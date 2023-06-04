/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - fit_me
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`fit_me` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `fit_me`;

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `dress_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `count` varchar(50) DEFAULT NULL,
  `expected_date` varchar(50) DEFAULT NULL,
  `description` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`booking_id`,`date`,`user_id`,`dress_id`,`status`,`count`,`expected_date`,`description`) values (1,'2021-01-03',3,3,'assigned','5','05-03-2021','hhshsh'),(2,'2021-02-04',1,4,'completed','4','06-03-2021','sjsjkla'),(3,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'2021-10-13',5,6,'pending','3','2021-8-23','sgsgsg'),(6,'2021-11-18',12,3,'completed','1','2021-11-17','shshs'),(8,'2021-11-18',12,6,'completed','5','2222','ffgf'),(9,'2022-02-28',12,3,'assigned','14','23-2-2022','gshhsjs'),(10,'2022-03-01',7,3,'completed','1','22-3-2022','ss'),(11,'2022-03-01',7,3,'assigned','1','22-3-2022','ss'),(12,'2022-03-01',12,6,'assigned','2','17-3-2022','hh'),(13,'2022-03-01',12,3,'completed','1','18-3-2022','hhhh'),(14,'2022-03-02',12,3,'completed','1','4-3-2022','Chinese'),(15,'2022-03-02',12,3,'completed','2','5-3-2022','double stich ');

/*Table structure for table `booking_assign` */

DROP TABLE IF EXISTS `booking_assign`;

CREATE TABLE `booking_assign` (
  `assign_id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) DEFAULT NULL,
  `tailor_id` int(11) DEFAULT NULL,
  `assign_date` varchar(50) DEFAULT NULL,
  `end_date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`assign_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `booking_assign` */

insert  into `booking_assign`(`assign_id`,`booking_id`,`tailor_id`,`assign_date`,`end_date`,`status`) values (3,2,6,'2021-08-30','2021-08-11','completed'),(5,6,6,'2021-11-18','2021-11-25','pending'),(6,1,6,'2022-02-28','2022-03-02','pending'),(7,2,16,'2022-02-28','2022-03-03','completed'),(8,9,6,'2022-02-28','2022-03-02','pending'),(9,10,6,'2022-03-01','2022-03-17','completed'),(10,11,6,'2022-03-01','2022-03-22','pending'),(11,13,16,'2022-03-01','2022-03-30','completed'),(12,12,8,'2022-03-01','2022-04-15','pending'),(13,14,16,'2022-03-02','2022-03-06','completed'),(14,15,15,'2022-03-02','2022-03-05','completed');

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`chat_id`,`date`,`time`,`from_id`,`to_id`,`message`) values (1,'2022-03-01','16:07:23',12,0,'hello'),(2,'2022-03-01','16:07:24',0,12,'hi'),(3,'2022-03-01','16:07:25',0,12,'Etnhaaa'),(4,'2022-03-01','16:08:01',12,0,'ooii'),(5,'2022-03-01',NULL,0,12,'hello'),(6,'2022-03-01',NULL,0,12,'hiii'),(7,'2022-03-01','16:34:49',0,1,'dfgdgdfgdf'),(8,'2022-03-01','16:34:58',0,7,'dsfdsfsd'),(9,'2022-03-01','16:37:38',0,1,'dfgdfgdfgdf'),(10,'2022-03-01','16:37:40',0,1,'dfgdfgdfgdf'),(11,'2022-03-01','16:38:10',0,1,'cvbcvbcvbcv'),(12,'2022-03-01','16:38:13',0,1,'dfgdsfsdfds'),(13,'2022-03-01','16:38:50',0,1,'dsgdsgdgdg'),(14,'2022-03-01','16:38:53',0,1,'gdfgdfgdfg'),(15,'2022-03-01','16:39:48',12,0,'gshshss'),(16,'2022-03-01','16:39:59',12,0,'hsjjsjsd'),(17,'2022-03-01','16:40:37',0,7,'mmknkjbnkj'),(18,'2022-03-01','16:41:47',7,0,'dfg'),(19,'2022-03-01','16:41:49',0,7,'dfgdfgdf'),(20,'2022-03-01','16:41:55',7,0,'gggg'),(21,'2022-03-01','16:42:04',0,7,'aaaa'),(22,'2022-03-01','16:42:08',7,0,'hi'),(23,'2022-03-01','16:44:24',0,1,'zfsdfdsfdsf'),(24,'2022-03-01','16:44:29',0,3,'dsfsdfsd'),(25,'2022-03-02','14:47:30',0,1,'jjghg'),(26,'2022-03-02','14:47:41',12,0,'hi');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `complaint` varchar(200) DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`date`,`user_id`,`complaint`,`reply`,`status`) values (1,'2021-08-26',3,'lkjhgfd','ok','replied'),(9,'2022-03-01',12,'HH hhe i','pending','pending'),(10,'2022-03-01',12,'hhh hhhsuw fussyksd bsylssb feysyss stwyssdy gwtsyd gsysy','pending','pending');

/*Table structure for table `dress` */

DROP TABLE IF EXISTS `dress`;

CREATE TABLE `dress` (
  `dress_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`dress_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `dress` */

insert  into `dress`(`dress_id`,`name`) values (3,'Shirt'),(4,'Pants'),(5,'trouser'),(6,'kurta'),(7,'tuxedo');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`type`) values (1,'qwert','2233','user'),(3,'plmn','2233','user'),(4,'dhggfgh@gmail.com','1','tailor'),(5,'dhggfgh@gmail.com','7896541236','tailor'),(6,'djdjh@gmail.com','1234','tailor'),(7,'shosh@gmail.com','2222','user'),(8,'jdhkjwhwe@gmail.com','222','tailor'),(9,'admin','abc','admin'),(10,'','','tailor'),(11,'xer','a','tailor'),(12,'sougandhrs2001@gmail.com','4567','user'),(13,'com.google.android.material.textfield.TextInputEdi','com.google.android.material.textfield.TextInputEdi','user'),(14,'hdnd','hjdh','user'),(15,'shone@gmail.com','7383899333','tailor'),(16,'shine@gmail.com','1234','tailor'),(17,'ramesh24@gmail.com','abc','user'),(18,'rakesh@gmail.com','7383899999','tailor');

/*Table structure for table `measurement` */

DROP TABLE IF EXISTS `measurement`;

CREATE TABLE `measurement` (
  `measurement_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `m1` varchar(50) DEFAULT NULL,
  `m2` varchar(50) DEFAULT NULL,
  `m3` varchar(50) DEFAULT NULL,
  `m4` varchar(50) DEFAULT NULL,
  `m5` varchar(50) DEFAULT NULL,
  `m6` varchar(50) DEFAULT NULL,
  `m7` varchar(50) DEFAULT NULL,
  `m8` varchar(50) DEFAULT NULL,
  `m9` varchar(50) DEFAULT NULL,
  `m10` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`measurement_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;

/*Data for the table `measurement` */

insert  into `measurement`(`measurement_id`,`user_id`,`m1`,`m2`,`m3`,`m4`,`m5`,`m6`,`m7`,`m8`,`m9`,`m10`) values (18,1,'(39.43514079092751+0j)','(30.171179133116077+0j)','(24.64840479438416+0j)','(35.76514309477765+0j)','(19.317694939485644+0j)','(21.664294417498017+0j)','(34.68945302433731+0j)','(40.47102852839353+0j)','(34.68945302433731+0j)','(40.70089454833634+0j)'),(52,12,'46.48344648355512','38.06881564899919','25.2136558903241','38.5546220720169','25.472697859981103','21.288176530153883','50.4273117806482','31.595242923207532','50.54673385633698','31.595242923207532');

/*Table structure for table `tailor` */

DROP TABLE IF EXISTS `tailor`;

CREATE TABLE `tailor` (
  `tailor_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `dob` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `house` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  `image` varchar(350) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tailor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `tailor` */

insert  into `tailor`(`tailor_id`,`name`,`dob`,`gender`,`email`,`phone`,`house`,`post`,`pin`,`image`,`login_id`) values (4,'shonaru','2021-08-22','female','djdjh@gmail.com','7896541732','iehgfjke2','jgdjfk2','245422','/static/tailor_image/2.PNG',6),(5,'sougandhiiii','2021-08-04','male','jdhkjwhwe@gmail.com','2013597862','sougu7','vadakara','672018','/static/tailor_image/7.PNG',8),(6,'shone','2000-12-02','male','shone@gmail.com','7383899333','haahahaha','pududps','673122','/static/tailor_image/logo.jpg',15),(7,'Shine','2008-02-15','male','shine@gmail.com','7383895555','shinr','madapu','369852','/static/tailor_image/Free Tailor Logo Designs.png',16),(8,'rakesh','1998-02-14','male','rakesh@gmail.com','7383899999','tttt','dddd','314598','/static/tailor_image/logo.jpg',18);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `house` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  `image` varchar(350) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`user_id`,`name`,`gender`,`email`,`phone`,`house`,`post`,`city`,`pin`,`image`,`login_id`) values (1,'Hadique','female','soosusu@gmail.com','098765432','souuuu','vatkara','kozhikode','098778','/static/tailor_image/2.PNG',1),(2,'Shone','male','alihhaha@gmail.com','1234567899','hajaj','vattakinaru','kozhikode','789870','/static/tailor_image/4.PNG',3),(3,'sougandh','male','shosh@gmail.com','543216789','jaklla','kottooli','kozhikode','873939','/static/tailor_image/7.PNG',12),(4,'Jamal','male','sos@gmail.com','9876543210','jajoo','jake','rrki','292920','/static/tailor_image/7.PNG',2),(5,'Doms','Male','domu2001@gmail.com','9539990682','hmmm','mmm','nmmm','673102','/static/user_image/20220301_151743.jpg',11),(6,'ramesh','Male','ramesh24@gmail.com','9846789046','sbhsjjajjs','sjjww','ksksks','728293','/static/user_image/20220302_113422.jpg',17);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
