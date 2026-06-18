/* April 26, 2026. 11:10 p.m. */

CREATE TABLE users (
    email varchar(50) primary key,
    username varchar(16) unique,
    password varchar(16),
    description text
);

CREATE TABLE artists (
    id varchar(100) primary key,
    name varchar(100),
    picture varchar(500)
);

CREATE TABLE albums (
    artist_id varchar(100) references artists(id),
    id varchar(100) primary key,
    name varchar(100),
    cover varchar(500),
    release varchar(10)
);

CREATE TABLE tracks (
    album_id varchar(100) references albums(id),
    id varchar(100) primary key,
    track int,
    name varchar(100)
);

CREATE TABLE subgenres (
    id varchar(100) primary key,
    name varchar(20)
);

CREATE TABLE styles (
    id varchar(100) primary key,
    name varchar(20)
);

CREATE TABLE tags (
    id varchar(100) primary key,
    name varchar(20)
);

CREATE TABLE tracks_subgenres (
    id int primary key generated always as identity,
    track_id varchar(100) references tracks(id),
    subgenres_id varchar(100) references subgenres(id)
);

CREATE TABLE tracks_styles (
    id int primary key generated always as identity,
    track_id varchar(100) references tracks(id),
    styles_id varchar(100) references styles(id)
);

CREATE TABLE tracks_tags (
    id int primary key generated always as identity,
    track_id varchar(100) references tracks(id),
    tags_id varchar(100) references tags(id),
    user_id varchar(100) references users(username)
);

CREATE TABLE artist_scoring (
    artist_id varchar(100) references artists(id),
    username varchar(100) references users(username),
    score int not null,
    tier int,
    favorite boolean,
    primary key (artist_id, username)
);

CREATE TABLE album_scoring (
    album_id varchar(100) references albums(id),
    username varchar(100) references users(username),
    score int not null,
    tier int,
    favorite boolean,
    primary key (album_id, username)
);

CREATE TABLE track_scoring (
    track_id varchar(100) references tracks(id),
    username varchar(100) references users(username),
    score int not null,
    melody int,
    solo int,
    vocals int,
    tier int,
    favorite boolean,
    primary key (track_id, username)
);

CREATE VIEW artist AS
    SELECT
        artists.id AS artist_id,
        albums.id AS album_id,
        albums.name,
        albums.cover,
        albums.release
    
    FROM artists LEFT JOIN albums
    ON artists.id = albums.artist_id;

CREATE VIEW album AS
    SELECT
        albums.id AS album_id,
        tracks.id AS track_id,
        tracks.track,
        tracks.name
    FROM albums LEFT JOIN tracks
    ON albums.id = tracks.album_id;

CREATE VIEW track AS
    SELECT
        artists.id AS artist_id,
        artists.name AS artist_name,
        albums.id AS album_id,
        albums.name AS album_name,
        albums.cover,
        tracks.id,
        tracks.name
    FROM tracks LEFT JOIN albums
    ON albums.id = tracks.album_id
    LEFT JOIN artists
    ON albums.artist_id = artists.id;

/* 5:40 p.m. Starting view creation */
/* 7:00 p.m. Finished */
