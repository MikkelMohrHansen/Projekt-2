CREATE DATABASE IF NOT EXISTS DBSimpel;
use DBSimpel;

CREATE TABLE students(
    studentID int not null AUTO_INCREMENT,
    firstName VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    PRIMARY KEY (studentID)
);

CREATE TABLE rooms(
    roomID int not NULL AUTO_INCREMENT,
    roomName VARCHAR(50) NOT NULL,
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

CREATE TABLE teachers(
    teacherID INT not null AUTO_INCREMENT,
    mail VARCHAR(50),
    passW VARCHAR(50),
    PRIMARY KEY (teacherID)
);

INSERT INTO students(firstName, surname)
VALUES("Test", "Testson");

INSERT INTO rooms(roomName)
VALUES("lab");

INSERT INTO teachers(mail, passW)
VALUES("test@ucn.dk", "test");