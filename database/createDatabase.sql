CREATE TABLE Account(
	pseudonym VARCHAR(50),
	email VARCHAR(50) NOT NULL,
	password BYTEA NOT NULL,
	createdAt DATE NOT NULL,
	lastLoginAt DATE NOT NULL,
	birthDate DATE NOT NULL,
	picture VARCHAR(50) NOT NULL,
	biography VARCHAR(254),
	PRIMARY KEY(pseudonym),
	UNIQUE(email)
);

CREATE TABLE Document(
	path VARCHAR(50),
	Account VARCHAR(50) NOT NULL,
	type VARCHAR(50) NOT NULL,
	fileSize INT NOT NULL,
	createdAt DATE NOT NULL,
	lastModifiedAt DATE NOT NULL,
	lastVisitedAt VARCHAR(50) NOT NULL,
	description VARCHAR(254),
	pseudonym VARCHAR(50) NOT NULL,
	PRIMARY KEY(path),
	FOREIGN KEY(pseudonym) REFERENCES Account(pseudonym)
);

CREATE TABLE read(
	pseudonym VARCHAR(50),
	path VARCHAR(50),
	lastVisitedAt DATE NOT NULL,
	PRIMARY KEY(pseudonym, path),
	FOREIGN KEY(pseudonym) REFERENCES Account(pseudonym),
	FOREIGN KEY(path) REFERENCES Document(path)
);

CREATE TABLE Follow(
	pseudonym_Following VARCHAR(50),
	pseudonym_Followed VARCHAR(50),
	PRIMARY KEY(pseudonym_Following, pseudonym_Followed),
	FOREIGN KEY(pseudonym_Following) REFERENCES Account(pseudonym),
	FOREIGN KEY(pseudonym_Followed) REFERENCES Account(pseudonym)
);

CREATE TABLE Evaluate(
	pseudonym VARCHAR(50),
	path VARCHAR(50),
	rating BYTE NOT NULL,
	comment VARCHAR(254) NOT NULL,
	createdAt DATE NOT NULL,
	PRIMARY KEY(pseudonym, path),
	FOREIGN KEY(pseudonym) REFERENCES Account(pseudonym),
	FOREIGN KEY(path) REFERENCES Document(path)
);
