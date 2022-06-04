CREATE TABLE IF NOT EXISTS genre (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS musician (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS album (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL,
	release_year INTEGER CHECK(release_year <= DATE_PART('YEAR', CURRENT_TIMESTAMP)::INTEGER)
);

CREATE TABLE IF NOT EXISTS track (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL,
	duration time(0) NOT NULL,
	album_id INTEGER REFERENCES album(id)
);

CREATE TABLE IF NOT EXISTS collection (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL,
	release_year INTEGER CHECK(release_year <= DATE_PART('YEAR', CURRENT_TIMESTAMP)::INTEGER)
);

CREATE TABLE IF NOT EXISTS collection_track (
	collection_id INTEGER REFERENCES collection(id),
	track_id INTEGER REFERENCES track(id),
	CONSTRAINT pk_collection_track PRIMARY KEY (collection_id, track_id)
);

CREATE TABLE IF NOT EXISTS genre_musician (
	genre_id INTEGER REFERENCES genre(id),
	musician_id INTEGER REFERENCES musician(id),
	CONSTRAINT pk_genre_musician PRIMARY KEY (genre_id, musician_id)
);

CREATE TABLE IF NOT EXISTS album_musician (
	album_id INTEGER REFERENCES album(id),
	musician_id INTEGER REFERENCES musician(id),
	CONSTRAINT pk_album_musician PRIMARY KEY (album_id, musician_id)
);