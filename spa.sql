CREATE DATABASE spa;
USE spa;

CREATE TABLE `booking` (
`uid` int(11) NOT NULL,
`email` varchar(50) NOT NULL,
`name` varchar(50) NOT NULL,
`vtype` varchar(50) NOT NULL,
`slot` varchar(50) NOT NULL,
`date` date NOT NULL,
`vehicle` varchar(50) NOT NULL,
`number` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DELIMITER $$
CREATE TRIGGER `slotcancel` BEFORE DELETE ON `booking` FOR EACH ROW INSERT INTO trigr VALUES(null,OLD.uid,OLD.email,OLD.name,'SLOT CANCELLED',NOW())
$$
 
DELIMITER ; DELIMITER $$
CREATE TRIGGER `slotupdate` AFTER UPDATE ON `booking` FOR EACH ROW INSERT INTO trigr VALUES(null,NEW.uid,NEW.email,NEW.name,'SLOT UPDATED',NOW())
$$ DELIMITER ;
DELIMITER $$
CREATE TRIGGER `slotbook` AFTER INSERT ON `booking` FOR EACH ROW INSERT INTO
trigr VALUES(null,NEW.uid,NEW.email,NEW.name,'SLOT BOOKED',NOW())
$$ DELIMITER ;


CREATE TABLE `trigr` (
`tid` int(11) NOT NULL,
`pid` int(11) NOT NULL,
`email` varchar(50) NOT NULL,
`name` varchar(50) NOT NULL,
`action` varchar(50) NOT NULL,
`timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user` (
`id` int(11) NOT NULL,
`username` varchar(50) NOT NULL,
`email` varchar(50) NOT NULL,
`password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `booking`
ADD PRIMARY KEY (`uid`);


ALTER TABLE `trigr`
ADD PRIMARY KEY (`tid`);

ALTER TABLE `user`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `email` (`email`);


ALTER TABLE `booking`
MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;


ALTER TABLE `trigr`
MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
 

ALTER TABLE `user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
