# Bautista_Crepay-Lister




Good Day po Ma,am Glydel Here po is the sql code po para po gumana sa python salamat po




CREATE DATABASE crepay_lister;

USE crepay_lister;


CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
);

CREATE TABLE payment_reminders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    credit_account VARCHAR(50),
    amount DECIMAL(10, 2),
    next_payment_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);



CREATE TABLE workers_user( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);


