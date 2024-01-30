-- Basic Table Creation Script

CREATE DATABASE IF NOT EXISTS deti_shop
	CHARACTER SET = 'utf16';

USE deti_shop;

CREATE TABLE IF NOT EXISTS UserP -- Em vez de User devido a uma palavra reservada
(
	usrID			INT 
					NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
	first_name		VARCHAR(32)
					NOT NULL,
	last_name		VARCHAR(32)
					NOT NULL,
	username		VARCHAR(32)
					NOT NULL UNIQUE,
	email			VARCHAR(32)
					NOT NULL,
	passwd			VARCHAR(128) -- Tive de aumentar de 64 para 128 devido ao algoritmo do Argon2
					NOT NULL,
	descript		VARCHAR(4096), -- Misc. profile description
	phoneNum		INT, 
	perms			CHAR(1) -- Permission conveyed via a single letter -> U : normal client ; A : admin client
					NOT NULL
                	CHECK (perms = 'U' OR perms = 'A'),
	createDate		DATE
					NOT NULL,
	secretToken		CHAR(140) -- Encrypted TOTP secret token
					DEFAULT NULL,
	lastOTP			INT			-- Last OTP code input with this user's credentials
					DEFAULT 0,
	CONSTRAINT Usr_UniqName UNIQUE (first_name, last_name)
);

CREATE TABLE IF NOT EXISTS Category
(
	catID		INT
				NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
	nome		VARCHAR(128)
				UNIQUE
                NOT NULL
);

CREATE TABLE IF NOT EXISTS Product
(
	prodID		INT
				NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
	nome		VARCHAR(128)
				UNIQUE
                NOT NULL,
	price		DECIMAL(6,2)
				NOT NULL CHECK (0 < price),
	catID		INT
				NOT NULL,
	stock		INT
				NOT NULL
                CHECK (-1 < stock),
	descript	VARCHAR(4096),
    
    CONSTRAINT Prod_CatID_FK
		FOREIGN KEY (catID) REFERENCES Category (catID)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Request
(
	reqID			INT
					NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
	reqDate			DATE
					NOT NULL,
	reqUsrID		INT 
					NOT NULL,
	morada			VARCHAR(128)
					NOT NULL,
	reqStatus		INT			-- 0 : To be delivered ; 1 : Delivered
					NOT NULL
                    CHECK (reqStatus = 0 OR reqStatus = 1),
                    
	CONSTRAINT Request_UsrID_FK 
		FOREIGN KEY (reqUsrID) REFERENCES UserP (usrID)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Product_Request
(
	prodID			INT
					NOT NULL 
                    REFERENCES Product (prodID),
	reqID			INT 
					NOT NULL
                    REFERENCES Request (reqID),
	quant			DECIMAL(5,2)
					NOT NULL
					DEFAULT 1
                    CHECK (0 < quant),
                    
	CONSTRAINT ProdReq_PK PRIMARY KEY (prodID, reqID),
    
	CONSTRAINT ProdReq_ProdID_FK
		FOREIGN KEY (prodID) REFERENCES Product (prodID)
			ON DELETE CASCADE
            ON UPDATE CASCADE,
	CONSTRAINT ProdReq_ReqID_FK
		FOREIGN KEY (reqId)	REFERENCES Request (reqID)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS WishList
(
	prodID			INT
					NOT NULL,
	usrID			INT 
					NOT NULL,
                    
	CONSTRAINT WishList_PK PRIMARY KEY (prodID, usrID),
    
    CONSTRAINT WishList_ProdID_FK
		FOREIGN KEY (prodID) REFERENCES Product (prodID)
			ON DELETE CASCADE
            ON UPDATE CASCADE,
	CONSTRAINT WishList_UsrID_FK
		FOREIGN KEY (usrID)	REFERENCES UserP (usrID)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Cart
(
	prodID			INT
					NOT NULL,
	usrID			INT 
					NOT NULL,
	quant			DECIMAL(5,2)
					NOT NULL
					DEFAULT 1
                    CHECK (0 < quant),
	waiting_confirm INT
					NOT NULL
					CHECK (waiting_confirm = 0 OR waiting_confirm = 1)
					DEFAULT 0,
	morada			VARCHAR(128)
					DEFAULT NULL,
                    
	CONSTRAINT Cart_PK PRIMARY KEY (prodID, usrID),
    
	CONSTRAINT Cart_ProdID_FK
		FOREIGN KEY (prodID) REFERENCES Product (prodID)
			ON DELETE CASCADE
            ON UPDATE CASCADE,
	CONSTRAINT Cart_UsrID_FK
		FOREIGN KEY (usrID)	REFERENCES UserP (usrID)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Review
(
	reviewID	INT
				NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
	rating		INT
				NOT NULL
                CHECK (0 <= rating <= 10),
	critique	VARCHAR(4096),
	revDate		DATE
				NOT NULL,
	usrID		INT
				NOT NULL,
	prodID		INT
				NOT NULL,
	
	CONSTRAINT Rev_UsrID_FK
		FOREIGN KEY (usrID) REFERENCES UserP (usrID)
			ON DELETE CASCADE
            ON UPDATE CASCADE,
	CONSTRAINT Rev_ProdID_FK
		FOREIGN KEY (prodID) REFERENCES Product (prodID)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

SHOW WARNINGS;