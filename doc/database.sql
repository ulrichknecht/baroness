/* The database is a sqlite3 database

--displaying the column names for querries works with
.headers on

-- Table info can be shown with

PPRAGMA table_info(table_name);

--or

.schema

-- to play around with database and test data:

sqlite3 -init database.sql 

- to create a database with the test data declared in this file use:

$ sqlite3 -echo database.db < database.sql

-- The created database can be used with

$ sqlite3 database.db

-
*/

.headers on

-- The table Users contains user information, user information is what we want to know about the user, and his privileges

CREATE TABLE Users(
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	password TEXT NOT NULL,
	longname TEXT NOT NULL,
	email TEXT,
	rfid_id TEXT,
	isblack BOOLEAN DEFAULT 0,
	isbaron BOOLEAN DEFAULT 0,
	isshown BOOLEAN DEFAULT 1,
	autoblack BOOLEAN DEFAULT 1
);

-- The table PRODUCTS contains information about the beverages available
CREATE TABLE Products(
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	price REAL NOT NULL,
	isshown BOOLEAN DEFAULT 0
);

-- The table Consumed contains all products that have been consumed, who it consumend, when it was consumed,  and also if they have been payed allready, this is important because we do not want to have redunant data.
-- Maybe we add a column "dept" to users, then we have to remove the column ISPAYD ffrom this tabla

CREATE TABLE Consumed(
	id INTEGER PRIMARY KEY,
	prodnr INTEGER NOT NULL,
	consumer INTEGER NOT NULL,
	price REAL DEFAULT 0.0,
	time DATETIME,

	FOREIGN KEY(prodnr) REFERENCES Products(id),
	FOREIGN KEY(consumer) REFERENCES USERS(id)
);

-- The table Deposits contains all money deposits done by the users
CREATE TABLE Deposits(
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    amount REAL DEFAULT 0.0,
    time DATETIME,

    FOREIGN KEY(userid) REFERENCES USERS(id)
);

-- The table Config stores basic config data, this is for the admins and the barons



--------------------------------------------------------------------------------
-- Test data 
INSERT INTO Users(id,name,password,longname,email,rfid_id,isblack,isbaron,isshown) VALUES
	(1, 'petra',      'test', 'Petra Besser',        'petra@bess.er',    '0x0123456789', 0, 0, 1),
	(2, 'peter',      'test', 'Peter Schlechter',    'peter@schlecht.er','0x0987654321', 0, 0, 1),
	(3, 'hindenburg', 'test', 'Paul von Hindenburg', 'hind@enburg.er',   '0x6666666666', 0, 1, 1);


INSERT INTO Products(id,name,price,isshown) VALUES 
	(1, 'Bier',   1.0, 1),
	(2, 'Limo',   0.7, 1),
	(3, 'Makava', 1.0, 1);


INSERT INTO Consumed (prodnr, consumer, price, time) VALUES 
	(1, 1, 1.0, CURRENT_TIMESTAMP),
	(1, 1, 1.0, CURRENT_TIMESTAMP),
	(1, 1, 1.0, CURRENT_TIMESTAMP),
	(1, 1, 1.0, CURRENT_TIMESTAMP),
	(2, 1, 0.7, CURRENT_TIMESTAMP),
	(2, 1, 0.7, CURRENT_TIMESTAMP),
	(2, 1, 0.7, CURRENT_TIMESTAMP),
	(3, 3, 1.0, CURRENT_TIMESTAMP),
	(3, 3, 1.0, CURRENT_TIMESTAMP),
	(3, 3, 1.0, CURRENT_TIMESTAMP);

--Check if all data was correctly created:
SELECT * FROM Users;
SELECT * FROM Products;
SELECT * FROM Consumed;
