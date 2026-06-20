-- CREATE DATABASE personsdb;
-- USE personsdb;

CREATE DATABASE IF NOT EXISTS personsdb;
USE personsdb;

CREATE TABLE persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    isMale BOOLEAN NOT NULL
);

INSERT INTO persons (name, age, isMale)
VALUES
('John', 23, TRUE),
('Ann', 19, FALSE);