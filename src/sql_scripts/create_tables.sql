/* April 26, 2026. 11:10 p.m. */

CREATE TABLE users (
    id int primary key,
    name varchar(15)
);

CREATE TABLE artists (
    id int primary key,
    name varchar(50),
    picture varchar(500)
);

CREATE TABLE albums (
    id int primary key,
    artist_id int references artists(id),
    name varchar(50),
    cover varchar(500),
    release date
);

CREATE TABLE tracks (
    id int primary key,
    album_id int references albums(id),
    track int,
    name varchar(50)
);

CREATE TABLE subgenres (
    id int primary key,
    name varchar(20)
);

CREATE TABLE styles (
    id int primary key,
    name varchar(20)
);

CREATE TABLE tags (
    id int primary key,
    name varchar(20)
);

CREATE TABLE tracks_subgenres (
    id int primary key,
    track_id int references tracks(id),
    subgenre_id int references subgenres(id)
);

CREATE TABLE tracks_styles (
    id int primary key,
    track_id int references tracks(id),
    style_id int references subgenres(id)
);

CREATE TABLE tracks_tags (
    id int primary key,
    track_id int references tracks(id),
    tag_id int references subgenres(id),
    user_id int references users(id)
);

CREATE TABLE artist_scoring (
    id int primary key,
    artist_id int references artists(id),
    user_id int references users(id),
    score int not null,
    tier int,
    favorite boolean
);

CREATE TABLE album_scoring (
    id int primary key,
    album_id int references albums(id),
    user_id int references users(id),
    score int not null,
    tier int,
    favorite boolean
);

CREATE TABLE track_scoring (
    id int primary key,
    track_id int references tracks(id),
    user_id int references users(id),
    score int not null,
    melody int,
    solo int,
    vocals int,
    tier int,
    favorite boolean
);
