DROP TABLE IF EXISTS users;

CREATE TABLE users (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	    name TEXT NOT NULL,
	    email TEXT NOT NULL,
		password TEXT NOT NULL,
		image TEXT NOT NULL
);

INSERT INTO users (name, email, password, image)
values('Abdullah Adel', 'abdullahadel.aam@gmail.com', 'Abdullah123', 'abdullah.jpg');