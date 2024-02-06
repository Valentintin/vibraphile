/* this file contain the model of the data in sql... for every modification here, change model.py */

CREATE TABLE Account(
   pseudonym VARCHAR(16) ,
   email VARCHAR(50) NOT NULL,
   password VARCHAR(50) NOT NULL,
   createdat DATE NOT NULL,
   lastLoginat DATE NOT NULL,
   birthdate DATE NOT NULL,
   picture VARCHAR(50) NOT NULL,
   biography VARCHAR(254) ,
   PRIMARY KEY(pseudonym),
   UNIQUE(email)
);

CREATE TABLE Document(
   path VARCHAR(50) ,
   name VARCHAR(16) NOT NULL,
   type VARCHAR(50) NOT NULL,
   filesize INTEGER NOT NULL,
   createdat DATE NOT NULL,
   lastmodifiedat DATE NOT NULL,
   lastvisitedat DATE NOT NULL,
   description VARCHAR(254) ,
   pseudonym VARCHAR(16) NOT NULL,
   PRIMARY KEY(path),
   FOREIGN KEY(pseudonym) REFERENCES Account(pseudonym)
);

CREATE TABLE read(
   pseudonym VARCHAR(16) ,
   path VARCHAR(50) ,
   lastVisitedAt DATE NOT NULL,
   PRIMARY KEY(pseudonym, path),
   FOREIGN KEY(pseudonym) REFERENCES Account(pseudonym),
   FOREIGN KEY(path) REFERENCES Document(path)
);

CREATE TABLE Follow(
   pseudonymFollowed VARCHAR(16) ,
   pseudonymFollow VARCHAR(16) ,
   PRIMARY KEY(pseudonymFollow, pseudonymFollowed),
   FOREIGN KEY(pseudonymFollow) REFERENCES Account(pseudonym),
   FOREIGN KEY(pseudonymFollowed) REFERENCES Account(pseudonym)
);

CREATE TABLE Evaluate(
   pseudonym VARCHAR(16) ,
   path VARCHAR(50) ,
   rating SMALLINT NOT NULL,
   comment VARCHAR(254) NOT NULL,
   createdAt DATE NOT NULL,
   PRIMARY KEY(pseudonym, path),
   FOREIGN KEY(pseudonym) REFERENCES Account(pseudonym),
   FOREIGN KEY(path) REFERENCES Document(path)
);

/* for crypting password */
CREATE EXTENSION pgcrypto;
-- SELECT * FROM pg_available_extensions;