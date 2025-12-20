-- ---------------------------------
-- Book Haven DDL
-- ---------------------------------

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
    author_id INT IDENTITY(1,1) NOT NULL,
    name VARCHAR(200) NOT NULL
);
GO

-- Table: description
CREATE TABLE description (
    description_id INT IDENTITY(1,1) NOT NULL,
    description VARCHAR(MAX) NOT NULL
);
GO

-- Table: category
CREATE TABLE category (
    category_id INT IDENTITY(1,1) NOT NULL,
    category_name VARCHAR(100) NOT NULL
);
GO

-- Table: book
CREATE TABLE book (
    ISBN VARCHAR(40) NOT NULL,
    title VARCHAR(255) NOT NULL,
    publication_year INT,
    description_id INT
);
GO

-- Table: book_author
CREATE TABLE book_author (
    ISBN VARCHAR(40) NOT NULL,
    author_id INT NOT NULL
);
GO

-- Table: book_category
CREATE TABLE book_category (
    ISBN VARCHAR(40) NOT NULL,
    category_id INT NOT NULL
);
GO

-- Table: book_copy
CREATE TABLE book_copy (
    copy_id INT IDENTITY(1,1) NOT NULL,
    status VARCHAR(50),
    condition VARCHAR(100),
    price NUMERIC(10,2),
    ISBN VARCHAR(40) NOT NULL
);
GO

-- Table: member
CREATE TABLE member (
    member_id INT IDENTITY(1,1) NOT NULL,
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    street VARCHAR(100),
    bdate DATE
);
GO

-- Table: staff
CREATE TABLE staff (
    staff_id INT IDENTITY(1,1) NOT NULL,
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) NOT NULL,
    role VARCHAR(100),
    password VARCHAR(255) NOT NULL,
    salary NUMERIC(10,2)
);
GO

-- Table: reservation
CREATE TABLE reservation (
    reservation_id INT IDENTITY(1,1) NOT NULL,
    member_id INT NOT NULL,
    staff_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    returned_at DATE
);
GO

-- Table: reservation_details
CREATE TABLE reservation_details (
    reservation_id INT NOT NULL,
    copy_id INT NOT NULL,
    position_in_queue INT NOT NULL
);
GO


-- ---------------------------------
-- 2. PRIMARY KEYS
-- ---------------------------------

-- PK for author
ALTER TABLE author ADD CONSTRAINT PK_author PRIMARY KEY (author_id);
GO

-- PK for description
ALTER TABLE description ADD CONSTRAINT PK_description PRIMARY KEY (description_id);
GO

-- PK for category
ALTER TABLE category ADD CONSTRAINT PK_category PRIMARY KEY (category_id);
GO

-- PK for book
ALTER TABLE book ADD CONSTRAINT PK_book PRIMARY KEY (ISBN);
GO

-- PK for book_author (composite key)
ALTER TABLE book_author ADD CONSTRAINT PK_book_author PRIMARY KEY (ISBN, author_id);
GO

-- PK for book_category (composite key)
ALTER TABLE book_category ADD CONSTRAINT PK_book_category PRIMARY KEY (ISBN, category_id);
GO

-- PK for book_copy
ALTER TABLE book_copy ADD CONSTRAINT PK_book_copy PRIMARY KEY (copy_id);
GO

-- PK for member
ALTER TABLE member ADD CONSTRAINT PK_member PRIMARY KEY (member_id);
GO

-- PK for staff
ALTER TABLE staff ADD CONSTRAINT PK_staff PRIMARY KEY (staff_id);
GO

-- PK for reservation
ALTER TABLE reservation ADD CONSTRAINT PK_reservation PRIMARY KEY (reservation_id);
GO

-- PK for reservation_details (composite key)
ALTER TABLE reservation_details ADD CONSTRAINT PK_reservation_details PRIMARY KEY (reservation_id, copy_id);
GO


-- ---------------------------------
-- 3. UNIQUE CONSTRAINTS
-- ---------------------------------

-- Unique category_name
ALTER TABLE category ADD CONSTRAINT UQ_category_name UNIQUE (category_name);
GO

-- Unique member email
ALTER TABLE member ADD CONSTRAINT UQ_member_email UNIQUE (email);
GO

-- Unique member phone
ALTER TABLE member ADD CONSTRAINT UQ_member_phone UNIQUE (phone);
GO

-- Unique staff email
ALTER TABLE staff ADD CONSTRAINT UQ_staff_email UNIQUE (email);
GO

-- Unique staff phone
ALTER TABLE staff ADD CONSTRAINT UQ_staff_phone UNIQUE (phone);
GO


-- ---------------------------------
-- 4. FOREIGN KEYS
-- ---------------------------------

-- FK: book → description
ALTER TABLE book
    ADD CONSTRAINT FK_book_description
    FOREIGN KEY (description_id)
    REFERENCES description(description_id);
GO

-- FK: book_author → book
ALTER TABLE book_author
    ADD CONSTRAINT FK_book_author_book
    FOREIGN KEY (ISBN)
    REFERENCES book(ISBN);
GO

-- FK: book_author → author
ALTER TABLE book_author
    ADD CONSTRAINT FK_book_author_author
    FOREIGN KEY (author_id)
    REFERENCES author(author_id);
GO

-- FK: book_category → book
ALTER TABLE book_category
    ADD CONSTRAINT FK_book_category_book
    FOREIGN KEY (ISBN)
    REFERENCES book(ISBN);
GO

-- FK: book_category → category
ALTER TABLE book_category
    ADD CONSTRAINT FK_book_category_category
    FOREIGN KEY (category_id)
    REFERENCES category(category_id);
GO

-- FK: book_copy → book
ALTER TABLE book_copy
    ADD CONSTRAINT FK_book_copy_book
    FOREIGN KEY (ISBN)
    REFERENCES book(ISBN);
GO

-- FK: reservation → member
ALTER TABLE reservation
    ADD CONSTRAINT FK_reservation_member
    FOREIGN KEY (member_id)
    REFERENCES member(member_id);
GO

-- FK: reservation → staff
ALTER TABLE reservation
    ADD CONSTRAINT FK_reservation_staff
    FOREIGN KEY (staff_id)
    REFERENCES staff(staff_id);
GO

-- FK: reservation_details → reservation
ALTER TABLE reservation_details
    ADD CONSTRAINT FK_res_details_reservation
    FOREIGN KEY (reservation_id)
    REFERENCES reservation(reservation_id);
GO

-- FK: reservation_details → book_copy
ALTER TABLE reservation_details
    ADD CONSTRAINT FK_res_details_copy
    FOREIGN KEY (copy_id)
    REFERENCES book_copy(copy_id);
GO


-- Create the SQL Server Login (The credential to connect to the server)
USE master;
GO
CREATE LOGIN flask_book_user WITH
    PASSWORD = '123456',
    CHECK_POLICY = ON,      
    DEFAULT_DATABASE = [Book_haven];
GO

--  Create the Database User
USE [Book_haven];
GO

CREATE USER [flask_book_user] FOR LOGIN [flask_book_user];
GO

-- Step 3: Grant Permissions (Allows the user to read and write data)
-- Granting only necessary permissions for a web application is a security best practice.
EXEC sp_addrolemember 'db_datareader', 'flask_book_user';
EXEC sp_addrolemember 'db_datawriter', 'flask_book_user';
-- GRANT EXECUTE TO flask_book_user;
GO
