CREATE DATABASE IF NOT EXISTS LogunitDB;
use LogunitDB;

CREATE TABLE UddannelsesHold(
    uddannelseID int not NULL AUTO_INCREMENT,
    uddannelseNavn varchar (70),
    tidsPunkt TIME,
    PRIMARY KEY (uddannelseID)
);

CREATE TABLE Students(
    studentID int not NULL AUTO_INCREMENT,
    navn varchar(255) NOT NULL,
    uddannelseID int,
    opstartsDato DATE,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (studentID),
    FOREIGN KEY (uddannelseID) REFERENCES UddannelsesHold(uddannelseID)
);

CREATE TABLE Lokaler(
    lokaleID int NOT NULL AUTO_INCREMENT,
    lokaleNavn varchar (255) NOT NULL,
    PRIMARY KEY (lokaleID)
);

CREATE TABLE Underviser(
    underviserID int NOT NULL AUTO_INCREMENT,
    email varchar (70),
    password varchar (70),
    uddannelseID int,
    FOREIGN KEY (uddannelseID) REFERENCES UddannelsesHold(uddannelseID),
    PRIMARY KEY (underviserID)
);


CREATE TABLE Checkind(
    studentID int NOT NULL,
    lokaleID int NOT NULL,
    checkIn TIMESTAMP,
    FOREIGN KEY (lokaleID) REFERENCES Lokaler(lokaleID),
    FOREIGN KEY (studentID) REFERENCES Students(studentID),
    PRIMARY KEY (studentID, checkIn)
);
CREATE TABLE UnderviserHold(
    underviserID int NOT NULL,
    uddannelseID int,
    FOREIGN KEY (underviserID) REFERENCES Underviser (underviserID),
    FOREIGN KEY (uddannelseID) REFERENCES UddannelsesHold (uddannelseID),
    PRIMARY KEY (underviserID, uddannelseID)
);

INSERT INTO UddannelsesHold(uddannelseNavn, tidspunkt)
VALUES("IT-Teknolog", '8:30:00');

INSERT INTO Students(navn)
VALUES("Test_Testson");

INSERT INTO Lokaler(lokaleNavn)
VALUES("lab");

INSERT INTO Underviser(email, password)
VALUES("test@ucn.dk", "test");