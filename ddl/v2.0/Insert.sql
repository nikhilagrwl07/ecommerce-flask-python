INSERT INTO `user` (`userid`, `fname`, `lname`, `password`, `active`, `address1`, `address2`, `city`, `state`, `country`, `zipcode`, `email`, `phone`, `image_file`, `isadmin`, `created_on`)
VALUES
	(1, 'Nikhil', 'Agrawal', '827ccb0eea8a706c4c34a16891f84e7b', 1, '', '', 'Chicago', 'IL', 'US', '60660', 'nikhil.agrwl07@gmail.com', '1234567', 'default.jpg', 0, '2018-12-03 11:49:36'),
	(4, 'User2', 'LastName2', '827ccb0eea8a706c4c34a16891f84e7b', 1, '6030 N SHERIDAN ROAD', 'APT 811', 'CHICAGO', 'Illinois', 'United States', '60660', 'nikhil.agrwl071@gmail.com', '3123638771', 'default.jpg', 0, '2018-12-03 11:53:20');

INSERT INTO `product` (`productid`, `sku`, `product_name`, `description`, `image`, `quantity`, `discounted_price`, `regular_price`, `product_rating`, `product_review`)
VALUES
	(2, '123', 'Iphone-X', 'Iphone-X', 'Iphone-10.png', 2, 499.0, 499.0, 0.0, NULL),
	(3, '234', 'SamsungUHD', 'SAMSUNG UN43NU6900 43\" CLASS/42.5\" DIAG 4K UHD MR120 SMART TV HDR 10+ PUR COLOR', 'SamsungUHD.jpg', 1, 499.0, 499.0, 0.0, NULL),
	(4, '456', 'SamsungS8', 'SamsungS8', 'SamsungS8.jpeg', 1, 599.0, 499.0, 0.0, NULL),
	(5, '678', 'motorolaZ2-Force', 'motorolaZ2-Force', 'motorolaZ2-Force.png', 2, 999.0, 499.0, 0.0, NULL),
	(9, '8910', 'SamsungCurved', '65\" Class Q8C Curved QLED 4K TV', 'SamsungCurved.jpg', 1, 699.0, 499.0, 0.0, NULL),
	(14, '101112', 'Macbook', 'Macbook', 'Macbook.jpg', 1, 4999.0, 499.0, 0.0, NULL),
	(15, '121314', 'Apple Watch', 'applewatch', 'applewatch.jpeg', 1, 10490.0, 499.0, 0.0, NULL);



INSERT INTO `category` (`categoryid`, `category_name`, `date_posted`)
VALUES
	(1, 'Mobiles', '2018-12-02 14:23:28'),
	(2, 'TV, Appliances, Electronics', '2018-12-02 14:23:28'),
	(3, 'Computers', '2018-12-02 14:23:28'),
	(4, 'Watches', '2018-12-02 14:23:28');


INSERT INTO `product_category` (`categoryid`, `productid`, `created_on`)
VALUES
	(1, 4, '2018-12-02 17:08:53'),
	(1, 5, '2018-12-02 14:43:59'),
	(2, 3, '2018-12-02 14:43:59'),
	(2, 9, '2018-12-02 14:43:59'),
	(3, 14, '2018-12-02 14:43:59'),
	(4, 15, '2018-12-02 14:43:59');



INSERT INTO `cart` (`userid`, `productid`, `quantity`)
VALUES
	(1, 2, 2);
