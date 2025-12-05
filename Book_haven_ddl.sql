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

-- Table: category
CREATE TABLE category (
    category_id INT IDENTITY(1,1),
    category_name VARCHAR(100) NOT NULL
);

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

-- Table: staff
CREATE TABLE staff (
    staff_id INT IDENTITY(1,1),
    fname VARCHAR(100) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    modified_at DATETIME2 DEFAULT GETDATE()
);

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

-- Table: book_author 
CREATE TABLE book_author (
    book_id INT NOT NULL,
    author_id INT NOT NULL
);

-- Table: book_category 
CREATE TABLE book_category (
    book_id INT NOT NULL,
    category_id INT NOT NULL
);

-- Table: reservation_details 
CREATE TABLE reservation_details (
    reservation_id INT NOT NULL,
    book_id INT NOT NULL,
    position_in_queue INT NOT NULL
);


-- ---------------------------------
-- 2.1. PRIMARY KEY Constraints
-- ---------------------------------

ALTER TABLE author
    ADD CONSTRAINT PK_author PRIMARY KEY (author_id);

ALTER TABLE category
    ADD CONSTRAINT PK_category PRIMARY KEY (category_id);

ALTER TABLE member
    ADD CONSTRAINT PK_member PRIMARY KEY (member_id);

ALTER TABLE staff
    ADD CONSTRAINT PK_staff PRIMARY KEY (staff_id);

ALTER TABLE book
    ADD CONSTRAINT PK_book PRIMARY KEY (book_id);

ALTER TABLE reservation
    ADD CONSTRAINT PK_reservation PRIMARY KEY (reservation_id);

-- Composite Primary Keys
ALTER TABLE book_author
    ADD CONSTRAINT PK_book_author PRIMARY KEY (book_id, author_id);

ALTER TABLE book_category
    ADD CONSTRAINT PK_book_category PRIMARY KEY (book_id, category_id);

ALTER TABLE reservation_details
    ADD CONSTRAINT PK_reservation_details PRIMARY KEY (reservation_id, book_id);


-- ---------------------------------
-- 2.2. UNIQUE Constraints
-- ---------------------------------

ALTER TABLE category
    ADD CONSTRAINT UQ_category_name UNIQUE (category_name);

ALTER TABLE member
    ADD CONSTRAINT UQ_member_phone UNIQUE (phone);
ALTER TABLE member
    ADD CONSTRAINT UQ_member_email UNIQUE (email);

ALTER TABLE staff
    ADD CONSTRAINT UQ_staff_phone UNIQUE (phone);
ALTER TABLE staff
    ADD CONSTRAINT UQ_staff_email UNIQUE (email);


-- ---------------------------------
-- 2.3. FOREIGN KEY Constraints
-- ---------------------------------

-- Table: reservation
ALTER TABLE reservation
    ADD CONSTRAINT FK_reservation_member FOREIGN KEY (member_id)
    REFERENCES member (member_id);

-- staff_id is nullable in the model
ALTER TABLE reservation
    ADD CONSTRAINT FK_reservation_staff FOREIGN KEY (staff_id)
    REFERENCES staff (staff_id);

-- Table: book_author
ALTER TABLE book_author
    ADD CONSTRAINT FK_book_author_book FOREIGN KEY (book_id)
    REFERENCES book (book_id);
ALTER TABLE book_author
    ADD CONSTRAINT FK_book_author_author FOREIGN KEY (author_id)
    REFERENCES author (author_id);

-- Table: book_category
ALTER TABLE book_category
    ADD CONSTRAINT FK_book_category_book FOREIGN KEY (book_id)
    REFERENCES book (book_id);
ALTER TABLE book_category
    ADD CONSTRAINT FK_book_category_category FOREIGN KEY (category_id)
    REFERENCES category (category_id);

-- Table: reservation_details
ALTER TABLE reservation_details
    ADD CONSTRAINT FK_res_details_reservation FOREIGN KEY (reservation_id)
    REFERENCES reservation (reservation_id);
ALTER TABLE reservation_details
    ADD CONSTRAINT FK_res_details_book FOREIGN KEY (book_id)
    REFERENCES book (book_id);