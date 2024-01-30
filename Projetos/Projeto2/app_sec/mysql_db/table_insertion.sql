USE deti_shop;

INSERT INTO UserP(first_name, last_name, username, email, passwd, descript, phoneNum, perms, createDate) VALUES 
	(
		'João',
		'Paulo',
        'jpaulo',
        'jpaulo@detioverlord.pt',
        '$argon2id$v=19$m=65536,t=3,p=4$4OQc6cXENT5ouVW7QEzRjA$E1/bMLWXS6ZoUMp5MA1tW6hyUTpgYfZTSxF0jkUJPrw', -- jeff
		'L, 256orem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
		111222333,
        'U',
        '1984-10-2'
    ),
    (
		'Iris', 
		'Santos',
        'irsantos',
        'dog@gmail.com',
        '$argon2id$v=19$m=65536,t=3,p=4$e7Vm6XImkykutlfi0POmCg$EKh9t35zI6ekqSaE0y12wwGsc9njoF6xHpzBQK438H4', -- georgetown
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
        333222111, 
        'U',
        '2003-11-2'
	),
    (
		'Isaac', 
        'Abrão',
        'isaacabr',
        'jefffan203@uatwo.pt',
        '$argon2id$v=19$m=65536,t=3,p=4$d2j5KKXHs68uBMXq+hXxCw$U4irmosDS4WIEiwGAHQIbgCBrQ4w/HhbcpdZ4R6nB9I', -- porttown
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
        999888777, 
        'U',
        '103-12-9'
	),
    (
		'Paul', 
		'Goodman',
        'itsaulgoodman',
        'breaking@bad.us',
        '$argon2id$v=19$m=65536,t=3,p=4$yneFqyVwByNYDzCMgv7q2A$uonHzNTKbngJtdBTiFwV08MJuQLaID5LcmsA9NdAhm0', -- saul badman
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
        101101101, 
        'U',
        '2000-01-01'
	),
    (
		'Saul', 
		'Bateman',
        'jasbate',
        'admin@deti.pt',
        '$argon2id$v=19$m=65536,t=3,p=4$jWuTTEzzhD15RSG2u/E4PQ$UYEh5y7fbAUHBlmm+emz1y4YHSjtjkwB+JqCCWVWlck', -- ios0203.
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
        010010010, 
        'U',
        '1990-10-20'
	),
    (
		'John', 
        'Smith',
        'jsmith',
        'realadmin@deti.pt',
        '$argon2id$v=19$m=65536,t=3,p=4$+KHuY3VIaDW7uG3SYtNVMA$hbWzm+Dfe9avFYpYZKEKway/7myl781g5v2V+GPX4tM', -- matrix1002-
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
        987273102, 
        'A',
        '1999-06-10'
	),
    (
		'Herald', 
        'Smithsonian',
        'smiths',
        'smither@yahoo.com',
        '$argon2id$v=19$m=65536,t=3,p=4$VZx3i3Kb/k+PuC1GGUOHyw$8jRqo18ggzZRgRXbVwCHqSkUZ6mJClDPOXg2u2gJbgc', -- George_herald!1083
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' ,
        999888000, 
        'A',
        '1884-04-10'
	)
;

INSERT INTO Category(nome) VALUES
	(
        'Clothing'
	),
	(
		'FootWear'
    ),
	(
		'Eletronics'
    ),
	(
		'Utilities'
    ),
    (
        'Furniture'
    )
;
    
INSERT INTO Product(nome, price, catID, stock, descript) VALUES
	(
		'DETI T-Shirt',
        12.25,
        1,
        124,
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' 
	),
    (
		'DETI Sweather',
        10.00,
        1, 
        15,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
	),
    (
		'DETI Kispo',
        32.99,
        1,
        20,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Balaclava',
        5,
        1,
        200,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI FlipFlops',
        5.99,
        2,
        100,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'NEI Socks',
        3.50,
        2,
        250,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Shoes',
        35,
        2,
        10,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Fins',
        9.99,
        2,
        50,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'NEECT mousepad',
        1.99,
        3,
        20,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'NEECT Breadboard',
        3,
        3,
        150,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'GLUA Raspberry',
        55,
        3,
        25,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Headphones',
        27.99,
        3,
        42,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'NEEET Grill',
        75,
        4,
        13,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Mug', 
        2.99,
        4,
        10,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
	),
    (
		'AETTUA Mop', 
        11.99,
        4, 
        11,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
	),
    (
		'LEA Plant',
        4.99,
        4,
        120,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Table',
        32.5,
        5,
        20,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI Lava Lamp',
        10,
        5,
        50,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'DETI ChalkBoard',
        150,
        5,
        4,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),
    (
		'LEI Chair',
        21.35,
		5, 
        8,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
	)
;

INSERT INTO Request(reqDate, reqUsrID, morada, reqStatus) VALUES
	(
		'2023-12-10',
        2,
        'nº125, Avenida do Mar',
        0
    ),
    (
		'2023-10-20',
        1,
        'nº10, Rua 25 de abril',
        1
    ),
    (
		'2023-07-25',
        6,
        'nº90, Travessa das Salinas',
        1
    )
;

INSERT INTO Product_Request(prodID, reqID, quant) VALUES
	(
		1,
        1,
        2
	),
    (
		2,
        1,
        1
	),
    (
		2,
        2,
        2
    ),
    (
		3,
        2,
        3
    ),
    (
		4,
        2,
        1
    ),
    (
		5,
        3,
        10
    )
;

INSERT INTO WishList(prodID,usrID) VALUES
	(
		1,
        5
    ),
    (
		4,
        5
    ),
    (
		6,
        4
    ),
    (
		4,
        4
    )
;

INSERT INTO Cart(prodID, usrID, quant) VALUES
	(
		2,
        1,
        10
    ),
    (
		4,
        1,
        2
    ),
    (
		3,
        3,
        5
    ),
    (
		5,
        3,
        3
    )
;

INSERT INTO Review(rating, critique, revDate, usrID, prodID) VALUES
	(
		0,
        'HATRED',
        '2023-07-30',
        6,
        5
    ),
    (
		10,
        'good :)',
        '2023-11-01',
        1,
        2
    )
;

SHOW ERRORS;