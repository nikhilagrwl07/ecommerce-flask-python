CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `address1` varchar(100) NOT NULL,
  `address2` varchar(100) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `country` varchar(20) NOT NULL,
  `zipcode` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `image_file` varchar(20) NOT NULL DEFAULT 'default.jpg',
  `isadmin` tinyint(1) NOT NULL DEFAULT '0',
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;


CREATE TABLE `category` (
  `categoryid` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  `date_posted` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`categoryid`),
  UNIQUE KEY `categoryName` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;



CREATE TABLE `product` (
  `productid` int(11) NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `image` text NOT NULL,
  `quantity` int(5) NOT NULL,
  `discounted_price` decimal(10,1) NOT NULL DEFAULT '0.0',
  `regular_price` decimal(10,1) NOT NULL DEFAULT '0.0',
  `product_rating` decimal(3,1) NOT NULL DEFAULT '0.0',
  `product_review` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

CREATE TABLE `product_category` (
  `categoryid` int(11) NOT NULL,
  `productid` int(11) NOT NULL,
  `created_on` date DEFAULT NULL,
  constraint pk_Product_Category primary key (`categoryid`,`productid`),
  constraint fk_Product_Category_1 FOREIGN KEY (`categoryid`) REFERENCES category (`categoryid`),
  constraint fk_Product_Category_2 FOREIGN KEY (`productid`) REFERENCES product (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `cart` (
  `userid` int(11) NOT NULL,
  `productid` int(11) NOT NULL,
  `quantity` int(5) NOT NULL,
  PRIMARY KEY (`userid`,`productid`),
  KEY `cart_ibfk_2` (`productid`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `order` (
  `orderid` int(11) NOT NULL AUTO_INCREMENT,
  `order_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_price` decimal(4,1) NOT NULL DEFAULT 0.00,
  `userid`  int(11) NOT NULL,
  PRIMARY KEY (`orderid`),
  constraint fk_Order_1 FOREIGN KEY (userid) REFERENCES user (userid)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


CREATE TABLE `ordered_product` (
  `ordproductid` int(11) NOT NULL AUTO_INCREMENT,
  `orderid` int(11) NOT NULL,
  `productid` int(11) NOT NULL,
  `quantity` int(5) NOT NULL,
  PRIMARY KEY (`ordproductid`),
  CONSTRAINT `ordered_product_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `order` (`orderid`),
  CONSTRAINT `ordered_product_ibfk_2` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


CREATE TABLE `sale_transaction` (
  `transactionid` int(11) NOT NULL AUTO_INCREMENT,
  `orderid` int(11) NOT NULL,
  `transaction_date` date NOT NULL,
  `amount` decimal(4,1) NOT NULL DEFAULT 0.00,
  `cc_number` varchar(50) NOT NULL,
  `cc_type` varchar(50) NOT NULL,
  `response` varchar(50) NOT NULL,
  PRIMARY KEY (`transactionid`),
  CONSTRAINT `sale_transaction_ibfk_1` FOREIGN KEY (`orderid`) REFERENCES `order` (`orderid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
