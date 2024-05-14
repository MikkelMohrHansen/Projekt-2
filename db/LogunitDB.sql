CREATE DATA IF NOT EXISTS LogunitDB;
use LogunitDB;

CREATE TABLE Students(
    studentID int not NULL AUTO_INCREMENT,
    navn varchar(255) NOT NULL,
    uddannelseID int NOT NULL,
    opstartsDato DATE,
    PRIMARY KEY (studentID)
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
    FOREIGN KEY (uddannelseID) REFERENCES UddannelsesHold(uddannelseID)
)

CREATE TABLE UddannelsesHold(
    uddannelseID int not NULL AUTO_INCREMENT,
    uddannelseNavn varchar (70),
    tidsPunkt DATE
    PRIMARY KEY (tidsPunkt)
)

CREATE TABLE Checkind(
    studentID int NOT NULL,
    lokaleID int NOT NULL,
    checkIn TIMESTAMP,
    FOREIGN KEY (lokaleID) REFERENCES Lokaler(lokaleID),
    FOREIGN KEY (studentID) REFERENCES Students(studentID),
    PRIMARY KEY (studentID)
)
CREATE TABLE underviserHold(
    underviserID int NOT NULL,
    uddannelseID INT NOT NULL,
    FOREIGN KEY (underviserID) REFERENCES Underviser (underviserID),
    FOREIGN KEY (uddannelseID) REFERENCES UddannelsesHold (uddannelseID),
    PRIMARY KEY (underviserID, uddannelseID)
)