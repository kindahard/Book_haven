-- ---------------------------------
-- Book haven DDL
-- ---------------------------------

-- Database Setup
USE master;
GO

CREATE DATABASE Book_haven;
GO

USE Book_haven;
GO

-- ---------------------------------
-- 1. TABLE CREATION 
-- ---------------------------------

-- Table: author
CREATE TABLE author (
    author_id INT IDENTITY(1,1),
    fname VARCHAR(100),
    lname VARCHAR(100)
);
GO

-- Table: category
CREATE TABLE category (
    category_id INT IDENTITY(1,1),
    category_name VARCHAR(100) NOT NULL
);
GO

-- Table: member
CREATE TABLE member (
    member_id INT IDENTITY(1,1),
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    street VARCHAR(100),
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    modified_at DATETIME2 DEFAULT GETDATE()
);
GO

-- Table: staff
CREATE TABLE staff (
    staff_id INT IDENTITY(1,1),
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) NOT NULL,    
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    modified_at DATETIME2 DEFAULT GETDATE()
);
GO

-- Table: book
CREATE TABLE book (
    book_id INT IDENTITY(1,1),
    title VARCHAR(255) NOT NULL,
    total_copies INT NOT NULL,
    available_copies INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    description VARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    modified_at DATETIME2 DEFAULT GETDATE()
);
GO

-- Table: reservation
CREATE TABLE reservation (
    reservation_id INT IDENTITY(1,1),
    member_id INT,
    staff_id INT,
    total_price NUMERIC(10, 2) NOT NULL,
    reservation_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    modified_at DATETIME2 DEFAULT GETDATE()
);
GO

-- Table: book_author 
CREATE TABLE book_author (
    book_id INT NOT NULL,
    author_id INT NOT NULL
);
GO

-- Table: book_category 
CREATE TABLE book_category (
    book_id INT NOT NULL,
    category_id INT NOT NULL
);
GO

-- Table: reservation_details 
CREATE TABLE reservation_details (
    reservation_id INT NOT NULL,
    book_id INT NOT NULL,
    position_in_queue INT NOT NULL
);
GO



-- ---------------------------------
-- PRIMARY KEY Constraints
-- ---------------------------------

ALTER TABLE author ADD CONSTRAINT PK_author PRIMARY KEY (author_id);
GO

ALTER TABLE category ADD CONSTRAINT PK_category PRIMARY KEY (category_id);
GO

ALTER TABLE member ADD CONSTRAINT PK_member PRIMARY KEY (member_id);
GO

ALTER TABLE staff ADD CONSTRAINT PK_staff PRIMARY KEY (staff_id);
GO

ALTER TABLE book ADD CONSTRAINT PK_book PRIMARY KEY (book_id);
GO

ALTER TABLE reservation ADD CONSTRAINT PK_reservation PRIMARY KEY (reservation_id);
GO

ALTER TABLE book_author ADD CONSTRAINT PK_book_author PRIMARY KEY (book_id, author_id);
GO

ALTER TABLE book_category ADD CONSTRAINT PK_book_category PRIMARY KEY (book_id, category_id);
GO

ALTER TABLE reservation_details ADD CONSTRAINT PK_reservation_details PRIMARY KEY (reservation_id, book_id);
GO


-- ---------------------------------
-- UNIQUE Constraints
-- ---------------------------------

ALTER TABLE category ADD CONSTRAINT UQ_category_name UNIQUE (category_name);
GO

ALTER TABLE member ADD CONSTRAINT UQ_member_phone UNIQUE (phone);
GO

ALTER TABLE member ADD CONSTRAINT UQ_member_email UNIQUE (email);
GO

ALTER TABLE staff ADD CONSTRAINT UQ_staff_phone UNIQUE (phone);
GO

ALTER TABLE staff ADD CONSTRAINT UQ_staff_email UNIQUE (email);
GO


-- ---------------------------------
-- FOREIGN KEY Constraints
-- ---------------------------------

ALTER TABLE reservation
    ADD CONSTRAINT FK_reservation_member FOREIGN KEY (member_id)
    REFERENCES member (member_id);
GO

ALTER TABLE reservation
    ADD CONSTRAINT FK_reservation_staff FOREIGN KEY (staff_id)
    REFERENCES staff (staff_id);
GO

ALTER TABLE book_author
    ADD CONSTRAINT FK_book_author_book FOREIGN KEY (book_id)
    REFERENCES book (book_id);
GO

ALTER TABLE book_author
    ADD CONSTRAINT FK_book_author_author FOREIGN KEY (author_id)
    REFERENCES author (author_id);
GO

ALTER TABLE book_category
    ADD CONSTRAINT FK_book_category_book FOREIGN KEY (book_id)
    REFERENCES book (book_id);
GO

ALTER TABLE book_category
    ADD CONSTRAINT FK_book_category_category FOREIGN KEY (category_id)
    REFERENCES category (category_id);
GO

ALTER TABLE reservation_details
    ADD CONSTRAINT FK_res_details_reservation FOREIGN KEY (reservation_id)
    REFERENCES reservation (reservation_id);
GO

ALTER TABLE reservation_details
    ADD CONSTRAINT FK_res_details_book FOREIGN KEY (book_id)
    REFERENCES book (book_id);
GO



-- ============================================
-- CREATE LOGIN AND USER FOR FLASK APP
-- ============================================

-- 1. Create SQL Server login at the server level
USE master;
GO

IF EXISTS (SELECT * FROM sys.sql_logins WHERE name = 'flask_user')
    DROP LOGIN flask_user;
GO

CREATE LOGIN flask_user 
WITH PASSWORD = '123456';
GO


-- 2. Create database user in Book_haven
USE Book_haven;
GO

IF EXISTS (SELECT * FROM sys.database_principals WHERE name = 'flask_user')
    DROP USER flask_user;
GO

CREATE USER flask_user FOR LOGIN flask_user;
GO


-- 3. Grant permissions to the user
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO flask_user;
GO


-- 4. Set default database for the login 
USE master;
GO
ALTER LOGIN flask_user WITH DEFAULT_DATABASE = Book_haven;
GO

PRINT 'Flask user created and permissions granted successfully.';
