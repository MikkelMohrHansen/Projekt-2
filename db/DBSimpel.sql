CREATE DATABASE DBSimpel;
use students;

CREATE TABLE students(
    studentID int not null AUTO_INCREMENT,
    firstName VARCHAR(50) NOT NULL;
    surname VARCHAR(50) NOT NULL;
    PRIMARY KEY (studentID)
);

CREATE TABLE rooms(
    roomID int not NULL AUTO_INCREMENT,
    roomName VARCHAR(50) NOT NULL;
    PRIMARY KEY (roomID)
);

CREATE TABLE attendTable (
    Date DATE,
    firstName VARCHAR(50),
    surname VARCHAR(50),
    roomName VARCHAR(50),
    studentID INT,
    PRIMARY KEY (studentID),
    FOREIGN KEY (studentID) REFERENCES students(studentID)
);

INSERT INTO students(firstName, surName)
VALUES("Test", "Testson");

INSERT INTO rooms(roomName)
VALUES("lab");