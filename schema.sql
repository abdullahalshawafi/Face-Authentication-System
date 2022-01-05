DROP TABLE IF EXISTS users;

CREATE TABLE users (
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	    name TEXT NOT NULL,
	    email TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL,
		image TEXT NOT NULL
);
-- .read schema.sql
INSERT INTO users (name, email, password, image)
VALUES
('Abdullah Adel', 'abdullahadel.aam@gmail.com', 'Abdullah123', 'abdullah.png'),
('Weaam Bassem', 'weaam.ali99@eng-st.cu.edu.eg', 'Weaam123', 'weaam.jpeg'),
('Robert Mounir', 'robertmounir66@gmail.com', 'Robert123', 'robert.jpeg'),
('Bishoy Atef', 'bishoyatef313@gmail.com', 'Bishoy123', 'bishoy.jpeg');